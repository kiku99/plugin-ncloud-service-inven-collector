import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector import AutoscalingConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.autoscaling.cloud_service import AutoscalingResource, AutoscalingResponse
from spaceone.inventory.model.compute.autoscaling.data import AutoScalingInfo
from spaceone.inventory.model.compute.autoscaling.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class AutoscalingManager(NaverCloudManager):
    connector_name = 'AutoscalingConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[AutoscalingResponse], List[ErrorResourceResponse]]:
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
        # adjustment_type = autoscaling_conn.list_adjustment_type()
        activity_log_list = autoscaling_conn.list_autoscaling_activity_log()
        configuration_log_list = autoscaling_conn.list_autoscaling_configuration_log()
        # scaling_policy_list = autoscaling_conn.list_scaling_process_type()
        launch_configuration_list = autoscaling_conn.list_launch_configuration()
        # process_list = autoscaling_conn.list_scaling_process_type()
        # scheduled_action_list = autoscaling_conn.list_scheduled_action()

        for autoscaling_group in autoscaling_groups:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                autoscaling_group_name = autoscaling_group.auto_scaling_group_name
                autoscaling_group_create_date = autoscaling_group.create_date
                launch_configuration_name = autoscaling_group.launch_configuration_name
                matched_activity_log_list = self._get_matched_activity_log_list(activity_log_list, autoscaling_group_name)
                matched_configuration_log_list = self._get_matched_configuration_log_list(configuration_log_list, autoscaling_group_name)
                matched_launch_configuration_list = self._get_matched_launch_configuration_list(launch_configuration_list, launch_configuration_name)

                autoscaling_group = {
                    'autoscalingGroup': {
                        'defaultCooldown': autoscaling_group.default_cooldown,
                        'desiredCapacity': autoscaling_group.desired_capacity,
                        'healthCheckGracePeriod': autoscaling_group.health_check_grace_period,
                        'healthCheckType': autoscaling_group.health_check_type.code,
                        # 'inAutoScalingGroupServerInstanceList': autoscaling_group.in_auto_scaling_group_server_instance_list,
                        # 'loadBalancerInstanceSummaryList': autoscaling_group.load_balancer_instance_summary_list,
                        'maxSize': autoscaling_group.max_size,
                        'minSize': autoscaling_group.min_size
                    },
                    'activityLogList': matched_activity_log_list,
                    'configurationLogList': matched_configuration_log_list,
                    'launchConfigurationList': matched_launch_configuration_list
                }

                ##################################
                # 2. Make Base Data
                ##################################
                autoscaling_data = AutoScalingInfo(autoscaling_group, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                autoscaling_resource = AutoscalingResource({
                    'name': autoscaling_group_name,
                    'launched_at': autoscaling_group_create_date,
                    'data': autoscaling_data
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(AutoscalingResponse({'resource': autoscaling_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] autoscaling_group_name => {autoscaling_group.auto_scaling_group_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Autoscaling', autoscaling_group_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    @staticmethod
    def _get_matched_activity_log_list(activity_log_list, autoscaling_group):
        activity_log_list_info = []

        for activity_log in activity_log_list:
            if autoscaling_group == activity_log.auto_scaling_group_name:
                activity_log = {
                    'activityNo': activity_log.activity_no,
                    'description': activity_log.description,
                    'details': activity_log.details,
                    'startTime': activity_log.start_time,
                    'endTime': activity_log.end_time,
                    'status': activity_log.status.code
                }
                activity_log_list_info.append(activity_log)

        return activity_log_list_info

    @staticmethod
    def _get_matched_configuration_log_list(configuration_log_list, autoscaling_group):
        configuration_log_list_info = []

        for configuration_log in configuration_log_list:
            if autoscaling_group == configuration_log.auto_scaling_group_name:
                configuration_log = {
                    'configurationActionName': configuration_log.configuration_action_name,
                    'configurationNo': configuration_log.configuration_no,
                    'launchConfigurationName': configuration_log.launch_configuration_name,
                    'scheduledActionName': configuration_log.scheduled_action_name,
                    'settingTime': configuration_log.setting_time
                }
                configuration_log_list_info.append(configuration_log)

        return configuration_log_list_info

    @staticmethod
    def _get_matched_launch_configuration_list(launch_configuration_list, launch_configuration_name):
        launch_configuration_list_info = []

        for launch_configuration in launch_configuration_list:
            if launch_configuration_name == launch_configuration.launch_configuration_name:
                launch_configuration = {
                    'launchConfigurationName': launch_configuration.launch_configuration_name,
                    'loginKeyName': launch_configuration.login_key_name,
                    # 'accessControlGroupList': launch_configuration.access_control_group_list
                }
                launch_configuration_list_info.append(launch_configuration)

        return launch_configuration_list_info
