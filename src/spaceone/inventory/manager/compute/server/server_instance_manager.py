import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.compute.server_connector import ServerConnector
from spaceone.inventory.manager.compute.server.server_instance.storage_manager_resource_helper import \
    StorageManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.login_key_manager_resource_helper import \
    LoginKeyManagerResourceHelper
# from spaceone.inventory.manager.compute.server.server_instance.loadbalancer_manager_resource_helper import \
#     LoadBalancerManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.nic_manager_resource_helper import \
    NICManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.server_instance_manager_resource_helper import \
    ServerInstanceManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.vpc_manager_resource_helper import \
    VPCManagerResourceHelper
from spaceone.inventory.model.compute.server.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.compute.server.cloud_service import server_instance, \
    ServerInstanceResponse, ServerInstanceResource
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
        # secret_data = params['secret_data']

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        self.instance_conn: ServerConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])
        all_resources = self.get_all_resources()
        compute_servers = self.instance_conn.list_Server_Instance()

        for compute_server in compute_servers:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                server_no = compute_server.server_instance_no
                zone, region = self._get_zone_and_region(compute_server)
                zone_info = {'zone': zone, 'region': region}

                ##################################
                # 2. Make Base Data
                ##################################
                resource = self.get_server_instance_resource(zone_info, compute_server, all_resources)

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(resource.get('region_code', ''))

                ##################################
                # 5. Make Resource Response Object
                # List of LoadBalancingResponse Object
                ##################################
                resource_responses.append(ServerInstanceResponse({'resource': resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {compute_server.server_instance_no}, error => {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Server', compute_server.server_instance_no)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    def get_all_resources(self) -> dict:
        # instancegroup_manager_helper: InstanceGroupManagerResourceHelper = InstanceGroupManagerResourceHelper(
        #     self.instance_conn)
        return {
            'storage': self.instance_conn.list_Storage_Instance(),
            'naver_cloud': self.instance_conn.list_autoscalers(),
            # 'instance_type': self.instance_conn.list_machine_types(),
            # 'instance_group': self.instance_conn.list_instance_group_managers(),
            # 'public_images': self.instance_conn.list_images(),
            # 'vpcs': self.instance_conn.list_vpcs(),
            # 'subnets': self.instance_conn.list_subnetworks(),
            # 'firewalls': self.instance_conn.list_firewall(),
            # 'forwarding_rules': self.instance_conn.list_forwarding_rules(),
            # 'target_pools': self.instance_conn.list_target_pools(),
            # 'url_maps': self.instance_conn.list_url_maps(),
            # 'backend_svcs': self.instance_conn.list_back_end_services(),
            # 'managed_instances_in_instance_groups': instancegroup_manager_helper.list_managed_instances_in_instance_groups()
        }

    def get_server_instance_resource(self, zone_info, instance, all_resources) -> ServerInstanceResource:
        """ Prepare input params for call manager """
        # VPC
        # vpcs = all_resources.get('vpcs', [])
        subnets = all_resources.get('subnets', [])

        # All Public Images
        public_images = all_resources.get('public_images', {})

        # URL Maps
        url_maps = all_resources.get('url_maps', [])
        backend_svcs = all_resources.get('backend_svcs', [])
        target_pools = all_resources.get('target_pools', [])

        # Forwarding Rules
        forwarding_rules = all_resources.get('forwarding_rules', [])

        # Firewall
        firewalls = all_resources.get('firewalls', [])

        # Get Instance Groups
        instance_group = all_resources.get('instance_group', [])

        # Get Machine Types
        instance_types = all_resources.get('instance_type', [])

        # Autoscaling group list
        autoscaler = all_resources.get('autoscaler', [])
        # instance_in_managed_instance_groups = all_resources.get('managed_instances_in_instance_groups', [])

        # storages
        storages = all_resources.get('storage', [])

        '''Get related resources from managers'''
        server_instance_manager_helper: ServerInstanceManagerResourceHelper = \
            ServerInstanceManagerResourceHelper(self.instance_conn)
        storage_manager_helper: StorageManagerResourceHelper = StorageManagerResourceHelper()
        login_key_manager_helper : LoginKeyManagerResourceHelper = LoginKeyManagerResourceHelper()

        storage_vos = storage_manager_helper.get_storage_info(instance, storages)
        login_key = login_key_manager_helper.get_naver_cloud_info(instance)
        server_data = server_instance_manager_helper.get_server_info(instance, zone_info)
        _name = instance.get('name', '')

        path, instance_type = instance.get('machineType').split('machineTypes/')

        ''' Gather all resources information '''
        '''
        server_data.update({
            'nics': nic_vos,
            'storages': storage_vos,
        })
        '''
        server_data['data'].update({
            'loginKey': login_key,
            'storage': storage_vos,
        })


        ##################################
        # 3. Make Return Resource
        ##################################
        server_data.update({
            'name': _name,
            'account': 'account',
            'instance_type': instance_type,
            'instance_size': server_data.get('data', {}).get('hardware', {}).get('core', 0),
            'launched_at': server_data.get('data', {}).get('compute', {}).get('launched_at', ''),
            'tags': 'labels',
            'reference': ReferenceModel({
                'resource_id': server_data['data']['google_cloud']['self_link'],
                'external_link': f"https://console.cloud.google.com/compute/instancesDetail/zones/{zone_info.get('zone')}/instances/{server_data['name']}?project={server_data['data']['compute']['account']}"
            })
        })
        return ServerInstanceResource(server_data, strict=False)

    @staticmethod
    def _get_zone_and_region(instance) -> (str, str):
        zone_name = instance.zone.zone_name
        region_name = instance.region.region_name
        return zone_name, region_name

    # def get_server_instance_resource(self, zone_info, compute_server, all_resources) -> ServerInstanceResource:
    #     return ServerInstanceResource(server_data, strict=False)
