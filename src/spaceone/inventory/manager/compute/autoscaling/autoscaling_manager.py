import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector import AutoscalingConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.autoscaling.cloud_service import AutoscalingResource, AutoscalingResponse
from spaceone.inventory.model.compute.autoscaling.data import AutoScalingGroup
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
                zone_list = self._get_zone_list(autoscaling_group.zone_list)
                matched_activity_log_list = self._get_matched_activity_log_list(activity_log_list,
                                                                                autoscaling_group_name)
                matched_configuration_log_list = self._get_matched_configuration_log_list(configuration_log_list,
                                                                                          autoscaling_group_name)
                matched_launch_configuration_list = self._get_matched_launch_configuration_list(
                    launch_configuration_list, launch_configuration_name)

                autoscaling_group = {
                    'default_cooldown': autoscaling_group.default_cooldown,
                    'desired_capacity': autoscaling_group.desired_capacity,
                    'health_check_grace_period': autoscaling_group.health_check_grace_period,
                    'health_check_type': autoscaling_group.health_check_type.code,
                    'zone_list': zone_list,
                    # 'inAutoScalingGroupServerInstanceList': autoscaling_group.in_auto_scaling_group_server_instance_list,
                    # 'loadBalancerInstanceSummaryList': autoscaling_group.load_balancer_instance_summary_list,
                    'max_size': autoscaling_group.max_size,
                    'min_size': autoscaling_group.min_size,
                    'activity_log_list': matched_activity_log_list,
                    'configuration_log_list': matched_configuration_log_list,
                    'launch_configuration_list': matched_launch_configuration_list
                }

                ##################################
                # 2. Make Base Data
                ##################################
                autoscaling_data = AutoScalingGroup(autoscaling_group, strict=False)

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
                error_response = self.generate_resource_error_response(e, 'Compute', 'Autoscaling',
                                                                       autoscaling_group_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    @staticmethod
    def _get_matched_activity_log_list(activity_log_list, autoscaling_group):
        activity_log_list_info = []

        for activity_log in activity_log_list:
            if autoscaling_group == activity_log.auto_scaling_group_name:
                activity_log = {
                    'activity_no': activity_log.activity_no,
                    'description': activity_log.description,
                    'details': activity_log.details,
                    'start_time': activity_log.start_time,
                    'end_time': activity_log.end_time,
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
                    'configuration_action_name': configuration_log.configuration_action_name,
                    'configuration_no': configuration_log.configuration_no,
                    'launch_configuration_name': configuration_log.launch_configuration_name,
                    'scheduled_action_name': configuration_log.scheduled_action_name,
                    'setting_time': configuration_log.setting_time
                }
                configuration_log_list_info.append(configuration_log)

        return configuration_log_list_info

    @staticmethod
    def _get_matched_launch_configuration_list(launch_configuration_list, launch_configuration_name):
        launch_configuration_list_info = []
        matched_access_control_group_list = []

        for launch_configuration in launch_configuration_list:
            for access_control_group in launch_configuration.access_control_group_list:
                access_control_group = {
                    'access_control_group_configuration_no': access_control_group.access_control_group_configuration_no,
                    'access_control_group_description': access_control_group.access_control_group_description,
                    'access_control_group_name': access_control_group.access_control_group_name,
                    'is_default_group': access_control_group.is_default_group
                }
                matched_access_control_group_list.append(access_control_group)

            if launch_configuration_name == launch_configuration.launch_configuration_name:
                launch_configuration = {
                    'launch_configuration_name': launch_configuration.launch_configuration_name,
                    'login_key_name': launch_configuration.login_key_name,
                    'access_control_group_list': matched_access_control_group_list
                }
                launch_configuration_list_info.append(launch_configuration)

        return launch_configuration_list_info

    @staticmethod
    def _get_zone_list(zone_list):
        zone_list_info = []

        for zone in zone_list:
            zone = {
                'zone_description': zone.zone_description,
                'zone_name': zone.zone_name,
                'zone_no': zone.zone_no
            }
        zone_list_info.append(zone)

        return zone_list_info
