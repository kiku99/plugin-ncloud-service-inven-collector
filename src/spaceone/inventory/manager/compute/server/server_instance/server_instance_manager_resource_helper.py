import logging

from spaceone.inventory.conf.cloud_service_conf import OAUTH_SCOPES
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.server.data import Compute, NaverCloud, OS, Hardware
from spaceone.inventory.connector.compute.server_instance_connector import ServerConnector

_LOGGER = logging.getLogger(__name__)


class ServerInstanceManagerResourceHelper(NaverCloudManager):
    connector_name = 'ServerConnector'
    instance_conn = None

    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: ServerConnector = ncloud_connector

    def get_server_info(self, instance, instance_types, disks, zone_info, public_images):
        """
        server_data = {'access_control_group_list': [],
                        'base_block_storage_disk_detail_type': {'code': 'HDD', 'code_name': 'HDD'},
                        'base_block_storage_disk_type': {'code': 'NET', 'code_name': 'Network Storage'},
                        'base_block_storage_size': 53687091200,
                        'block_device_partition_list': None,
                        'cpu_count': 1,
                        'create_date': '2023-08-13T15:57:59+0900',
                        'instance_tag_list': [],
                        'internet_line_type': None,
                        'is_fee_charging_monitoring': False,
                        'is_protect_server_termination': False,
                        'login_key_name': 'test-authkey',
                        'memory_size': 1073741824,
                        'platform_type': {'code': 'UBS64',
                        'code_name': 'Ubuntu Server 64 Bit'},
                        'port_forwarding_external_port': None,
                        'port_forwarding_internal_port': None,
                        'port_forwarding_public_ip': '101.101.165.122',
                        'private_ip': '10.41.74.229',
                        'public_ip': '',
                        'region': {'region_code': 'KR',
                        'region_name': 'Korea',
                        'region_no': '1'},
                        'server_description': '',
                        'server_image_name': 'ubuntu-18.04',
                        'server_image_product_code': 'SPSW0LINUX000130',
                        'server_instance_no': '18935302',
                        'server_instance_operation': {'code': 'NULL', 'code_name': 'Server NULL OP},
                        'server_instance_status': {'code': 'RUN', 'code_name': 'Server run state},
                        'server_instance_status_name': 'running',
                        'server_instance_type': {'code': 'MICRO', 'code_name': 'Micro Server'},
                        'server_name': 'test-sever',
                        'server_product_code': 'SPSVRSTAND000056',
                        'uptime': '2023-08-13T16:06:16+0900',
                        'user_data': '',
                        'zone': {'region_no': '1',
                                    'zone_code': 'KR-2',
                                    'zone_description': '평촌 zone',
                                    'zone_name': 'KR-2',
                                    'zone_no': '3'}}
        """

        os_data = self._get_os_data(instance, public_images)
        server_dic = self._get_server_dic(instance, zone_info)
        # google_cloud_data = self._get_google_cloud_data(instance, instance_in_managed_instance_groups)
        hardware_data = self._get_hardware_data(instance, instance_types, zone_info)
        compute_data = self._get_compute_data(instance, disks, zone_info)

        server_dic.update({
            'data': {
                'os': os_data,
                'google_cloud': 'google_cloud_data',
                'hardware': hardware_data,
                'compute': compute_data,
                'primary_ip_address': self._get_primary_ip_address(instance)
            }
        })
        return server_dic

    def _get_server_dic(self, instance, zone_info):
        server_data = {
            'name': instance.get('name', ''),
            'server_type': 'VM',
            'provider': 'google_cloud',
            'ip_addresses': self._get_ip_addresses(instance),
            'region_code': zone_info.get('region', '')
        }

        return server_data

    def _get_os_data(self, instance, public_images):

        disk_info = instance.get("disks", [])
        os_dists = disk_info[0].get('licenses', []) if len(disk_info) > 0 else []
        licenses = disk_info[0].get('licenses', []) if len(disk_info) > 0 else []
        os_type = "LINUX"
        os_identity = ''

        for idx, val in enumerate(os_dists):
            os_items = val.split("/")
            os_identity = os_items[-1].lower()
            if idx == 0:
                if "windows" in os_identity:
                    os_type = "WINDOWS"
                break

        os_data = self._get_appropriate_image_info(os_identity, licenses, public_images)
        os_data['os_type'] = os_type

        return OS(os_data, strict=False)

    @staticmethod
    def _get_appropriate_image_info(os_identity, licenses, public_images):
        # temp arch lists will be updated when full list has prepared.
        arch_list = ['x86_64', 'x86_32', 'x64', 'x86', 'amd64']
        os_data = {
            'details': '',
            'os_distro': '',
            'os_arch': ''
        }
        for key, images in public_images.items():
            find = False
            if key in os_identity:
                for image in images:
                    if licenses == image.get('licenses', []):
                        os_arch_index = [i for i, e in enumerate(arch_list) if e in image.get('description', '')]
                        os_data.update({'os_distro': 'windows-server' if key == 'windows' else key,
                                        'details': image.get('description', ''),
                                        'os_arch': arch_list[os_arch_index[0]] if len(os_arch_index) > 0 else ''})
                        find = True
                        break
            if find:
                break

        if os_identity == 'cos':
            os_data.update({'os_distro': 'cos',
                            'details': 'Google, Container-Optimized OS'})
        return os_data

    # def _get_google_cloud_data(self, instance, instance_in_managed_instance_groups):
    #     google_cloud = {
    #         "self_link": instance.get('selfLink', ''),
    #         "fingerprint": instance.get('fingerprint', ''),
    #         "reservation_affinity": self._get_reservation_affinity(instance),
    #         "deletion_protection": instance.get('deletionProtection', False),
    #         "scheduling": self._get_scheduling(instance),
    #         "tags": self.get_tag_items(instance.get('tags', {}).get('items', [])),
    #         "ssh_keys": self._get_ssh_keys(instance.get('metadata', {}).get('items', [])),
    #         "service_accounts": self._list_service_accounts(instance),
    #         "labels": self._get_labels(instance.get('labels', {})),
    #         'is_managed_instance': True if instance.get('selfLink',
    #                                                     '') in instance_in_managed_instance_groups else False,
    #     }
    #
    #     return GoogleCloud(google_cloud, strict=False)

    def _get_hardware_data(self, instance, instance_types, zone_info):
        """
        core = IntType(default=0)
        memory = FloatType(default=0.0)
        is_vm = StringType(default=True)
        cpu_model = ListType(StringType(default=""))
        """

        core, memory = self._get_core_and_memory(instance, instance_types)

        if core == 0 and memory == 0:
            core, memory = self._get_custom_image_type(instance, zone_info, instance_types)

        hardware_data = {
            'core': core,
            'memory': memory,
            'cpu_model': instance.get('cpuPlatform', ''),
            'is_vm': True
        }

        return Hardware(hardware_data, strict=False)

    def _get_compute_data(self, instance, disks, zone_info):
        """
            {
                'keypair': StringType(default="")
                'az':StringType()                       # zone_name
                'instance_id': StringType()
                'instance_name': StringType(default='')
                'instance_state':StringType(choices=('STAGING', 'RUNNING', 'STOPPING', 'REPAIRING'))
                'instance_type' : StringType()
                'account' : StringType()                  # Project_id
                'image' : StringType()
                'launched_at' : DateTimeType()
                'security_groups': []
                'tags' = DictType(StringType, default={})
            }
        """
        compute_data = {
            'keypair': '',
            'public_ip_address': self._get_public_ip_address(instance),
            'az': zone_info.get('zone', ''),  # zone_name
            'instance_id': instance.get('id'),
            'instance_name': instance.get('name', ''),
            'instance_state': instance.get('status'),
            'instance_type': self._get_instance_type(instance),
            'account': zone_info.get('project_id', ''),
            'image': self._get_images(instance, disks),
            'launched_at': instance.get('creationTimestamp'),
            'tags': self._get_tags_only_string_values(instance)
        }

        return Compute(compute_data)

    def _get_custom_image_type(self, instance, zone_info, instance_types):
        machine = instance.get('machineType', '')
        _machine = machine[machine.rfind('/') + 1:]

        custom_image_type = self.instance_conn.get_machine_type(zone_info.get('zone'), _machine)
        instance_types.append(custom_image_type)

        cpu = custom_image_type.get('guestCpus', 0)
        memory = round(float((custom_image_type.get('memoryMb', 0)) / 1024), 2)
        return cpu, memory

    @staticmethod
    def _get_tags_only_string_values(instance):
        tags = {}
        for k, v in instance.get('tags', {}).items():
            if isinstance(v, str):
                tags.update({k: v})
        return tags

    @staticmethod
    def _get_images(instance, disks):
        image = ''
        name = instance.get('name', '')

        for disk in disks:
            if name == disk.get('name', ''):
                _image = disk.get('sourceImage', '')
                image = _image[_image.rfind('/') + 1:]
                break
        return image

    @staticmethod
    def _get_instance_type(instance):
        machine_type = instance.get('machineType', '')
        machine_split = machine_type.split('/')
        return machine_split[-1]

    @staticmethod
    def _get_core_and_memory(instance, instance_types):
        machine_type = instance.get('machineType', '')
        _machine = machine_type[machine_type.rfind('/') + 1:]
        cpu = 0
        memory = 0
        for i_type in instance_types:
            if i_type.get('selfLink', '') == machine_type or i_type.get('name', '') == _machine:
                cpu = i_type.get('guestCpus')
                memory = round(float((i_type.get('memoryMb', 0)) / 1024), 2)
                break

        return cpu, memory

    @staticmethod
    def _get_primary_ip_address(instance):
        primary_ip_address = ''
        networks = instance.get('networkInterfaces', [])
        for i, v in enumerate(networks):
            if i == 0:
                primary_ip_address = v.get('networkIP', '')
                break
        return primary_ip_address

    @staticmethod
    def _get_public_ip_address(instance):
        public_ip_address = ''
        networks = instance.get('networkInterfaces', [])
        for i, v in enumerate(networks):
            if i == 0:
                access_configs = v.get('accessConfigs', [])
                for access_config in access_configs:
                    nat_ip = access_config.get('natIP', '')
                    if nat_ip != '':
                        public_ip_address = nat_ip
                        break
                break
        return public_ip_address

    @staticmethod
    def _get_ip_addresses(instance):
        ip_addresses = []
        networks = instance.get('networkInterfaces', [])
        for network in networks:
            private_ip = network.get('networkIP', '')
            access_configs = network.get('accessConfigs', [])
            if private_ip != '':
                ip_addresses.append(private_ip)

            for access_config in access_configs:
                nat_ip = access_config.get('natIP', '')
                if nat_ip != '':
                    ip_addresses.append(nat_ip)
        return ip_addresses

    @staticmethod
    def _get_reservation_affinity(instance):
        ra = instance.get('reservationAffinity', {})
        return ra.get('consumeReservationType', '')

    @staticmethod
    def _get_scheduling(instance):
        schedule = instance.get('scheduling', {})
        scheduling = {
            'on_host_maintenance': schedule.get('onHostMaintenance', 'MIGRATE'),
            'automatic_restart': schedule.get('automaticRestart', True),
            'preemptible': schedule.get('preemptible', False)
        }
        return scheduling

    @staticmethod
    def _get_labels(labels):
        changed_labels = []
        for label_key, label_value in labels.items():
            changed_labels.append({
                'key': label_key,
                'value': label_value
            })
        return changed_labels

    @staticmethod
    def get_tag_items(items):
        tags = []
        for item in items:
            tags.append({'key': item})
        return tags

    @staticmethod
    def _list_service_accounts(instance):
        access_policies = []
        if service_accounts := instance.get('serviceAccounts', []):
            for service_account in service_accounts:
                email = service_account.get('email', '')
                scopes = service_account.get('scopes', [])
                readable_scopes = []
                for scope in scopes:
                    try:
                        readable_scopes.append({'description': OAUTH_SCOPES[scope]})
                    except KeyError:
                        continue

                access_policies.append({
                    'service_account': email,
                    'display_name': 'Allow default access',
                    'scopes': readable_scopes
                })
        return access_policies

    @staticmethod
    def _get_ssh_keys(items):
        ssh_keys_info = {
            'ssh_keys': [],
            'block_project_ssh_keys': 'OFF'
        }
        if items:
            for item in items:
                if item['key'] == 'block-project-ssh-keys':
                    ssh_keys_info['block_project_ssh_keys'] = 'ON'
                if item['key'] == 'ssh-keys':
                    user_name, ssh_key = item['value'].split(':', 1)
                    ssh_keys_info['ssh_keys'].append({
                        'user_name': user_name,
                        'display_name': 'show',
                        'ssh_key': ssh_key
                    })
        return ssh_keys_info
