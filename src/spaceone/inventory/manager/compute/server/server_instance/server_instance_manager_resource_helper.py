import logging

from spaceone.inventory.conf.cloud_service_conf import OAUTH_SCOPES
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.server.data import Compute, Hardware, PortForwardingRules, IP
from spaceone.inventory.connector.compute.server_connector import ServerConnector

_LOGGER = logging.getLogger(__name__)


class ServerInstanceManagerResourceHelper(NaverCloudManager):
    connector_name = 'ServerConnector'
    instance_conn = None

    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: ServerConnector = ncloud_connector

    def get_server_info(self, instance, zone_info):
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

        server_dic = self._get_server_dic(instance, zone_info)
        hardware_data = self._get_hardware_data(instance)
        compute_data = self._get_compute_data(instance, zone_info)
        port_forwarding_rules = self._get_port_forwarding_rules(instance)
        ip_info = self._get_ip(instance)

        server_dic.update({
            'data': {
                'compute': compute_data,
                'portForwardingRules': port_forwarding_rules,
                'hardware': hardware_data,
                'ip': ip_info
            }
        })
        return server_dic

    @staticmethod
    def _get_server_dic(instance, zone_info):
        server_data = {
            'name': instance.server_name,
            'instance_type': instance.server_instance_type,
            'provider': 'naver_cloud',
            'region_code': zone_info.get('region', '')
        }

        return server_data

    @staticmethod
    def _get_hardware_data(instance):
        """
        cpu_count = IntType(default=0)
        memory_size = LongType(default=0.0)
        """

        cpu_count = instance.cpu_count
        memory_size = instance.memory_size

        hardware_data = {
            'cpuCount': cpu_count,
            'memorySize': memory_size,
        }

        return Hardware(hardware_data, strict=False)

    @staticmethod
    def _get_compute_data(instance, zone_info):
        # """
        #     {
        #         'serverName': instance.server_name,
        #         'serverImageName': instance.server_image_name,
        #         'serverInstanceStatus': instance.server_instance_status.code,  # zone_name
        #         'serverInstanceOperation': instance.server_instance_operation,
        #         'serverInstanceStatusName': instance.server_instance_status_name,
        #         'platformType': instance.platform_type,
        #         'createDate': instance.create_date,
        #         'uptime': instance.uptime,
        #         'serverImageProductCode': instance.server_image_product_code,
        #         'serverProductCode': instance.server_product_code,
        #         'serverInstanceType': instance.server_instance_type.code,
        #         'zone': zone_info.get('zone', ''),
        #         'region': zone_info.get('region', '')
        #     }
        # """

        compute_data = {
            'serverName': instance.server_name,
            'serverImageName': instance.server_image_name,
            'serverInstanceStatus': instance.server_instance_status.code,  # zone_name
            'serverInstanceOperation': instance.server_instance_operation.code,
            'serverInstanceStatusName': instance.server_instance_status_name,
            'platformType': instance.platform_type.code_name,
            'createDate': instance.create_date,
            'uptime': instance.uptime,
            'serverImageProductCode': instance.server_image_product_code,
            'serverProductCode': instance.server_product_code,
            'serverInstanceType': instance.server_instance_type.code,
            'zone': zone_info.get('zone', ''),
            'region': zone_info.get('region', '')
        }

        return Compute(compute_data, strict=False)

    @staticmethod
    def _get_port_forwarding_rules(instance):
        port_forwarding_rules_data = {
            'port_forwarding_external_port': instance.port_forwarding_external_port,
            'port_forwarding_internal_port': instance.port_forwarding_internal_port,
            'port_forwarding_public_ip': instance.port_forwarding_public_ip
        }

        return PortForwardingRules(port_forwarding_rules_data, strict=False)

    @staticmethod
    def _get_ip(instance):
        ip_data = {
            'private_ip': instance.private_ip,
            'public_ip': instance.public_ip
        }

        return IP(ip_data, strict=False)
