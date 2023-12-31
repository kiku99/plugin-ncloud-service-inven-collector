import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.connector.compute.server_connector import ServerConnector
from spaceone.inventory.manager.compute.server.server_instance.storage_manager_resource_helper import \
    StorageManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.login_key_manager_resource_helper import \
    LoginKeyManagerResourceHelper
from spaceone.inventory.manager.compute.server.server_instance.server_instance_manager_resource_helper import \
    ServerInstanceManagerResourceHelper
from spaceone.inventory.model.compute.server.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.compute.server.cloud_service import ServerInstanceResponse, ServerInstanceResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

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
        start_time = time.time()

        ##################################
        # 0. Gather All Related Resources
        ##################################
        self.instance_conn: ServerConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])
        all_resources = self.get_all_resources()
        compute_servers = self.instance_conn.list_server_instance()

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
                # 3. Make Collected Region Code
                ##################################
                self.set_region_code(resource.get('region', ''))

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(ServerInstanceResponse({'resource': resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {compute_server.server_instance_no}, error => {e}',
                              exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Compute', 'Server', server_no)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    def get_all_resources(self) -> dict:

        return {
            'storage': self.instance_conn.list_block_storage_instance(),
            'login_key': self.instance_conn.list_login_key(),
        }

    def get_server_instance_resource(self, zone_info, instance, all_resources) -> ServerInstanceResource:
        """ Prepare input params for call manager """

        ################## TBD ######################

        # storages
        storages = all_resources.get('storage', [])

        # login keys
        login_keys = all_resources.get('login_key', [])

        '''Get related resources from managers'''
        server_instance_manager_helper: ServerInstanceManagerResourceHelper = \
            ServerInstanceManagerResourceHelper(self.instance_conn)
        storage_manager_helper: StorageManagerResourceHelper = StorageManagerResourceHelper()
        login_key_manager_helper: LoginKeyManagerResourceHelper = LoginKeyManagerResourceHelper()

        storage_vos = storage_manager_helper.get_storage_info(instance, storages)
        login_key = login_key_manager_helper.get_login_key_info(login_keys)
        server_data = server_instance_manager_helper.get_server_info(instance, zone_info)
        account = login_key.key_name

        ''' Gather all resources information '''

        server_data['data'].update({
            'login_key': login_key,
            'storage': storage_vos,
        })

        server_data.update({
            'account': account,
            'instance_type': server_data.get('data', {}).get('compute', {}).get('server_instance_type', {}),
            'instance_size': server_data.get('data', {}).get('hardware', {}).get('cpu_count', 0),
            'launched_at': server_data.get('data', {}).get('compute', {}).get('create_date', '')
        })
        return ServerInstanceResource(server_data, strict=False)

    @staticmethod
    def _get_zone_and_region(instance) -> (str, str):
        zone_name = instance.zone.zone_name
        region_name = instance.region.region_name
        return zone_name, region_name
