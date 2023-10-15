import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.connector.networking.vpc_connector import NetworkingConnector
# from spaceone.inventory.manager.compute.server.server_instance.storage_manager_resource_helper import \
#     StorageManagerResourceHelper
# from spaceone.inventory.manager.compute.server.server_instance.login_key_manager_resource_helper import \
#     LoginKeyManagerResourceHelper
# from spaceone.inventory.manager.compute.server.server_instance.server_instance_manager_resource_helper import \
#     ServerInstanceManagerResourceHelper
from spaceone.inventory.model.networking.vpc_network.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.networking.vpc_network.cloud_service import ServerInstanceResponse, ServerInstanceResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class VPCNetworkManager(NaverCloudManager):
    connector_name = 'VPCNetworkConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[ServerInstanceResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** VPC Network START **')
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
        start_time = time.time()

        ##################################
        # 0. Gather All Related Resources
        ##################################

        self.vpc_conn: VPCNetworkManager = self.locator.get_connector(self.connector_name, **params)
        self.vpc_conn.set_connect(params['secret_data'])
        all_resources = self.get_all_resources()
        vpc_lists = self.vpc_conn.list_vpc()

        for vpc_list in vpc_lists:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                vpc_name = vpc_list.vpc_name_list
                zone, region = self._get_zone_and_region(vpc_lists)
                zone_info = {'zone': zone, 'region': region}

                ##################################
                # 2. Make Base Data
                ##################################
                resource = self.get_server_vpc_resource(zone_info, vpc_list, all_resources)

                ##################################
                # 3. Make Collected Region Code
                ##################################
                self.set_region_code(resource.get('region', ''))

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(ServerInstanceResponse({'resource': resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {vpc_list.server_instance_no}, error => {e}',
                              exc_info=True)
                error_response = self.generate_resource_error_response(e, 'VPCNetwork', 'Network', vpc_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    def get_all_resources(self) -> dict:

        return {
            'SubnetList': self.vpc_conn.list_Subnet(),
            'NetworkAclList': self.vpc_conn.Network_AclList(),
            'NatGatewayInstanceList': self.vpc_conn.List_Nat_Gateway_Instance(),
            'VpcPeeringInstanceList': self.vpc_conn.List_Vpc_Peering_Instance(),
            'RounteTableList': self.vpc_conn.List_Route_Talbe(),
        }

    def get_vpc_list(self, zone_info, instance, all_resources) -> ServerInstanceResource:
        """ Prepare input params for call manager """

        ################## TBD ######################

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

        # storages
        storages = all_resources.get('storage', [])

        # login keys
        login_keys = all_resources.get('loginKey', [])

        '''Get related resources from managers'''
        # server_instance_manager_helper: ServerInstanceManagerResourceHelper = \
        #     ServerInstanceManagerResourceHelper(self.instance_conn)
        # storage_manager_helper: StorageManagerResourceHelper = StorageManagerResourceHelper()
        # login_key_manager_helper: LoginKeyManagerResourceHelper = LoginKeyManagerResourceHelper()
        #
        # storage_vos = storage_manager_helper.get_storage_info(instance, storages)
        # login_key = login_key_manager_helper.get_login_key_info(login_keys)
        # server_data = server_instance_manager_helper.get_server_info(instance, zone_info)
        # account = login_key.keyName

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

        server_data.update({
            'account': account,
            'instance_type': server_data.get('data', {}).get('compute', {}).get('serverInstanceType', {}),
            'instance_size': server_data.get('data', {}).get('hardware', {}).get('cpuCount', 0),
            'launched_at': server_data.get('data', {}).get('compute', {}).get('createDate', '')
        })
        return ServerInstanceResource(server_data, strict=False)

    @staticmethod
    def _get_zone_and_region(instance) -> (str, str):
        zone_name = instance.zone.zone_name
        region_name = instance.region.region_name
        return zone_name, region_name