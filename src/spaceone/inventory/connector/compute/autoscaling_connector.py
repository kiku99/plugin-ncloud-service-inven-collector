import ncloud_autoscaling

from spaceone.inventory.libs.connector import NaverCloudConnector
from ncloud_server.rest import ApiException

__all__ = ['AutoscalingConnector']


class AutoscalingConnector(NaverCloudConnector):
    service = 'compute'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_adjustment_type(self):

        instance_list = []
        get_adjustment_type_list_request = ncloud_autoscaling.GetAdjustmentTypeListRequest()

        try:
            api_response = self.autoscaling_client.get_adjustment_type_list(get_adjustment_type_list_request)
            # print(api_response)
            for instance in api_response.adjustment_type_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_adjustment_type_list: %s\n" % e)

        return instance_list

    def list_autoscaling_activity_log(self):

        instance_list = []
        get_auto_scaling_activity_log_list_request = ncloud_autoscaling.GetAutoScalingActivityLogListRequest()
        try:
            api_response = self.autoscaling_client.get_auto_scaling_activity_log_list(get_auto_scaling_activity_log_list_request)
            for instance in api_response.activity_log_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_activity_log_list: %s\n" % e)

        return instance_list

    def list_autoscaling_configuration_log(self):

        instance_list = []
        get_auto_scaling_configuration_log_list_request = ncloud_autoscaling.GetAutoScalingConfigurationLogListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_configuration_log_list(get_auto_scaling_configuration_log_list_request)
            for instance in api_response.configuration_log_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_configuration_log_list: %s\n" % e)

        return instance_list

    def list_autoscaling_group(self):

        instance_list = []
        get_auto_scaling_group_list_request = ncloud_autoscaling.GetAutoScalingGroupListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_group_list(get_auto_scaling_group_list_request)
            for instance in api_response.auto_scaling_group_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_group_list: %s\n" % e)

        return instance_list

    def list_autoscaling_policy(self):

        instance_list = []
        get_auto_scaling_policy_list_request = ncloud_autoscaling.GetAutoScalingPolicyListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_policy_list(get_auto_scaling_policy_list_request)
            for instance in api_response.scaling_policy_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_policy_list: %s\n" % e)

        return instance_list

    def list_launch_configuration(self):

        instance_list = []
        get_launch_configuration_list_request = ncloud_autoscaling.GetLaunchConfigurationListRequest()

        try:
            api_response = self.autoscaling_client.get_launch_configuration_list(get_launch_configuration_list_request)
            for instance in api_response.launch_configuration_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_launch_configuration_list: %s\n" % e)

        return instance_list

    def list_scaling_process_type(self):

        instance_list = []
        get_scaling_process_type_list_request = ncloud_autoscaling.GetScalingProcessTypeListRequest()

        try:
            api_response = self.autoscaling_client.get_scaling_process_type_list(get_scaling_process_type_list_request)
            for instance in api_response.process_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_scaling_process_type_list: %s\n" % e)

        return instance_list

    def list_scheduled_action(self):

        instance_list = []
        get_scheduled_action_list_request = ncloud_autoscaling.GetScheduledActionListRequest()

        try:
            api_response = self.autoscaling_client.get_scheduled_action_list(get_scheduled_action_list_request)
            for instance in api_response.scheduled_update_group_action_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_scheduled_action_list: %s\n" % e)

        return instance_list





