import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector import AutoscalingConnector
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


class AutoscalingManager(NaverCloudManager):
    connector_name = 'AutoscalingConnector'
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
        self.instance_conn: AutoscalingConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])
        all_resources = self.get_all_resources()
        autoscaling_groups = self.instance_conn.list_autoscaling_group()

        for autoscaling_group in autoscaling_groups:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                autoscaling_group_name = autoscaling_group.auto_scaling_group_name
                zone = self._get_zone(autoscaling_group)
                zone_info = {'zone': zone}

                ##################################
                # 2. Make Base Data
                ##################################
                resource = self.get_autoscaling_resource(zone_info, autoscaling_group, all_resources)

                ##################################
                # 3. Make Collected Region Code
                ##################################
                # self.set_region_code(resource.get('region', ''))

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(ServerInstanceResponse({'resource': resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] autoscaling_group_name => {autoscaling_group.auto_scaling_group_name}, error => {e}',
                              exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Autoscaling', autoscaling_group_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    def get_all_resources(self) -> dict:

        return {
            'adjustmentType': self.instance_conn.list_adjustment_type(),
            'activityLogList': self.instance_conn.list_autoscaling_activity_log(),
            'configurationLogList': self.instance_conn.list_autoscaling_configuration_log(),
            'scalingPolicyList': self.instance_conn.list_scaling_process_type(),
            'launchConfigurationList': self.instance_conn.list_launch_configuration(),
            'processList': self.instance_conn.list_scaling_process_type(),
            'scheduledUpdateGroupActionList': self.instance_conn.list_scheduled_action()
        }

    def get_autoscaling_resource(self, zone_info, instance, all_resources) -> ServerInstanceResource:
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
        server_instance_manager_helper: ServerInstanceManagerResourceHelper = \
            ServerInstanceManagerResourceHelper(self.instance_conn)
        storage_manager_helper: StorageManagerResourceHelper = StorageManagerResourceHelper()
        login_key_manager_helper: LoginKeyManagerResourceHelper = LoginKeyManagerResourceHelper()

        storage_vos = storage_manager_helper.get_storage_info(instance, storages)
        login_key = login_key_manager_helper.get_login_key_info(login_keys)
        server_data = server_instance_manager_helper.get_server_info(instance, zone_info)
        account = login_key.keyName

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
    def _get_zone(instance) -> str:
        zone_name = instance.zone_list.zone_name
        return zone_name
