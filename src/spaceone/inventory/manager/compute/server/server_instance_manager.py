import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.compute.server_connector import ServerConnector
from spaceone.inventory.manager.compute.server.server_instance.instancegroup_manager_resource_helper import \
    InstanceGroupManagerResourceHelper
from spaceone.inventory.model.compute.server.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.compute.server.cloud_service import server_instance, \
    ServerInstanceResponse, ServerInstanceResource
from spaceone.inventory.model.compute.server.data import InstanceTag, InstanceTagList, InstanceGroup
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.libs.schema.base import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class ServerInstanceManager(NaverCloudManager):
    connector_name = 'ServerConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[ServerInstanceResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** Server START **')
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        resource_responses = []
        error_responses = []
        instance_id = ""

        start_time = time.time()
        secret_data = params['secret_data']
        #project_id = secret_data['project_id']

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        self.instance_conn: ServerConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])
        # all_resources = self.get_all_resources(project_id)
        compute_servers = self.instance_conn.list_Server_Instance()

        for compute_server in compute_servers:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                all_resources = self.get_all_resources()
                server_id = compute_server.get('id')
                # zone, region = self._get_zone_and_region(compute_server)
                # zone_info = {'zone': zone, 'region': region, 'project_id': project_id}

                ##################################
                # 2. Make Base Data
                ##################################
                # resource = self.get_server_instance_resource(project_id, zone_info, compute_server, all_resources)

                ##################################
                # 4. Make Collected Region Code
                ##################################
                # self.set_region_code(resource.get('region_code', ''))

                ##################################
                # 5. Make Resource Response Object
                # List of LoadBalancingResponse Object
                ##################################
                resource_responses.append(all_resources)

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {server_id}, error => {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Server', server_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses

    def get_all_resources(self) -> ServerInstanceResource:
        # instancegroup_manager_helper: InstanceGroupManagerResourceHelper = InstanceGroupManagerResourceHelper(
        #     self.instance_conn)
        server_data = self.instance_conn.list_Server_Instance()
        return ServerInstanceResource(server_data, strict=False)

    # def get_server_instance_resource(self, project_id, zone_info, instance, all_resources) -> ServerInstanceResource:
    #     """ Prepare input params for call manager """
    #     # VPC
    #     vpcs = all_resources.get('vpcs', [])
    #     subnets = all_resources.get('subnets', [])
    #
    #     # All Public Images
    #     public_images = all_resources.get('public_images', {})
    #
    #     # URL Maps
    #     url_maps = all_resources.get('url_maps', [])
    #     backend_svcs = all_resources.get('backend_svcs', [])
    #     target_pools = all_resources.get('target_pools', [])
    #
    #     # Forwarding Rules
    #     forwarding_rules = all_resources.get('forwarding_rules', [])
    #
    #     # Firewall
    #     firewalls = all_resources.get('firewalls', [])
    #
    #     # Get Instance Groups
    #     instance_group = all_resources.get('instance_group', [])
    #
    #     # Get Machine Types
    #     instance_types = all_resources.get('instance_type', [])
    #
    #     # Autoscaling group list
    #     autoscaler = all_resources.get('autoscaler', [])
    #     # instance_in_managed_instance_groups = all_resources.get('managed_instances_in_instance_groups', [])
    #
    #     # disks
    #     disks = all_resources.get('disk', [])
    #
    #     '''Get related resources from managers'''
    #     vm_instance_manager_helper: VMInstanceManagerResourceHelper = \
    #         VMInstanceManagerResourceHelper(self.instance_conn)
    #     auto_scaler_manager_helper: InstanceGroupManagerResourceHelper = \
    #         InstanceGroupManagerResourceHelper(self.instance_conn)
    #     loadbalancer_manager_helper: LoadBalancerManagerResourceHelper = LoadBalancerManagerResourceHelper()
    #     disk_manager_helper: DiskManagerResourceHelper = DiskManagerResourceHelper()
    #     nic_manager_helper: NICManagerResourceHelper = NICManagerResourceHelper()
    #     vpc_manager_helper: VPCManagerResourceHelper = VPCManagerResourceHelper()
    #     firewall_manager_helper: FirewallManagerResourceHelper = FirewallManagerResourceHelper()
    #     autoscaler_vo = auto_scaler_manager_helper.get_autoscaler_info(instance, instance_group, autoscaler)
    #     load_balancer_vos = loadbalancer_manager_helper.get_loadbalancer_info(instance, instance_group, backend_svcs,
    #                                                                           url_maps,
    #                                                                           target_pools, forwarding_rules)
    #     disk_vos = disk_manager_helper.get_disk_info(instance, disks)
    #     vpc_vo, subnet_vo = vpc_manager_helper.get_vpc_info(instance, vpcs, subnets)
    #     nic_vos = nic_manager_helper.get_nic_info(instance, subnet_vo)
    #     firewall_vos = firewall_manager_helper.list_firewall_rules_info(instance, firewalls)
    #
    #     firewall_names = [d.get('name') for d in firewall_vos if d.get('name', '') != '']
    #     server_data = vm_instance_manager_helper.get_server_info(instance, instance_types, disks, zone_info,
    #                                                              public_images, instance_in_managed_instance_groups)
    #     google_cloud_filters = [{'key': 'resource.labels.instance_id', 'value': instance.get('id')}]
    #     google_cloud = server_data['data'].get('google_cloud', {})
    #     _google_cloud = google_cloud.to_primitive()
    #     labels = _google_cloud.get('labels', [])
    #     _name = instance.get('name', '')
    #
    #     # Set GPU info
    #     if gpus_info := instance.get('guestAccelerators', []):
    #         gpus = self._get_gpu_info(gpus_info)
    #         server_data['data'].update({
    #             'gpus': gpus,
    #             'total_gpu_count': sum([gpu.get('gpu_count', 0) for gpu in gpus]),
    #             'has_gpu': True,
    #             'display': {'gpus': self._change_human_readable(gpus), 'has_gpu': True}
    #         })
    #
    #     path, instance_type = instance.get('machineType').split('machineTypes/')
    #
    #     ''' Gather all resources information '''
    #     '''
    #     server_data.update({
    #         'nics': nic_vos,
    #         'disks': disk_vos,
    #     })
    #     '''
    #     server_data['data'].update({
    #         'nics': nic_vos,
    #         'disks': disk_vos,
    #     })
    #     server_data['data']['compute']['security_groups'] = firewall_names
    #     server_data['data'].update({
    #         'load_balancers': load_balancer_vos,
    #         'security_group': firewall_vos,
    #         'autoscaler': autoscaler_vo,
    #         'vpc': vpc_vo,
    #         'subnet': subnet_vo,
    #         'google_cloud_monitoring': self.set_google_cloud_monitoring(project_id,
    #                                                                     "compute.googleapis.com/instance",
    #                                                                     instance.get('id'),
    #                                                                     google_cloud_filters),
    #         'google_cloud_logging': self.set_google_cloud_logging(project_id,
    #                                                               'gce_instance',
    #                                                               instance.get('id'),
    #                                                               google_cloud_filters)
    #     })
    #     ##################################
    #     # 3. Make Return Resource
    #     ##################################
    #     server_data.update({
    #         'name': _name,
    #         'account': project_id,
    #         'instance_type': instance_type,
    #         'instance_size': server_data.get('data', {}).get('hardware', {}).get('core', 0),
    #         'launched_at': server_data.get('data', {}).get('compute', {}).get('launched_at', ''),
    #         'tags': labels,
    #         'reference': ReferenceModel({
    #             'resource_id': server_data['data']['google_cloud']['self_link'],
    #             'external_link': f"https://console.cloud.google.com/compute/instancesDetail/zones/{zone_info.get('zone')}/instances/{server_data['name']}?project={server_data['data']['compute']['account']}"
    #         })
    #     })
    #     return ServerInstanceResource(server_data, strict=False)

    def _get_location(self, instance_group):
        if 'zone' in instance_group:
            url_zone = instance_group.get('zone')
            location = self.get_param_in_url(url_zone, 'zones')
        else:
            # zone or region key must be existed
            url_region = instance_group.get('region')
            location = self.get_param_in_url(url_region, 'regions')

        return location

    def get_instances(self, instances):
        _instances = []
        for instance in instances:
            url_instance = instance.get('instance', '')
            instance.update({'name': self.get_param_in_url(url_instance, 'instances')})
            _instances.append(instance)

        return _instances
