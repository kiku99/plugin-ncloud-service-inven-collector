import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector import AutoscalingConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.autoscaling.cloud_service import AutoscalingResource, AutoscalingResponse
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
        autoscaling_conn: AutoscalingConnector = self.locator.get_connector(self.connector_name, **params)
        autoscaling_conn.set_connect(params['secret_data'])

        autoscaling_groups = autoscaling_conn.list_autoscaling_group()
        adjustment_type = autoscaling_conn.list_adjustment_type()
        activity_log_list = autoscaling_conn.list_autoscaling_activity_log()
        configuration_log_list = autoscaling_conn.list_autoscaling_configuration_log()
        scaling_policy_list = autoscaling_conn.list_scaling_process_type()
        launch_configuration_list = autoscaling_conn.list_launch_configuration()
        process_list = autoscaling_conn.list_scaling_process_type()
        scheduled_action_list = autoscaling_conn.list_scheduled_action()

        for autoscaling_group in autoscaling_groups:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                autoscaling_group_name = autoscaling_group.auto_scaling_group_name

                autoscaling_group.update({
                    'autoscalingGroup':  {
                        'defaultCooldown'
                        'desiredCapacity'
                        'healthCheckGracePeriod'
                        'healthCheckType'
                        'inAutoScalingGroupServerInstanceList'
                        'load_balancer_instance_summary_list'
                        'max_size'

                    }
                    'activityLogList'
                    'configurationLogList'
                    'launchConfigurationList'
                })

                ##################################
                # 2. Make Base Data
                ##################################
                autoscaling_data = AutoscalingResource(autoscaling_group, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                autoscaling_resource = AutoscalingResource({
                    'name': autoscaling_group_name,
                    'launched_at': autoscaling_group.create_date,
                    'data': autoscaling_data,
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(AutoscalingResponse({'resource': autoscaling_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] autoscaling_group_name => {autoscaling_group.auto_scaling_group_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Autoscaling',
                                                                       autoscaling_group_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses
