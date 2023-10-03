import ncloud_autoscaling

from spaceone.inventory.libs.connector import NaverCloudConnector
from ncloud_server.rest import ApiException

__all__ = ['AutoscalingConnector']


class AutoscalingConnector(NaverCloudConnector):
    service = 'compute'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def List_Adjustment_Type(self):

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

    def List_Autoscaling_Activity_Log(self):

        instance_list = []
        get_auto_scaling_activity_log_list_request = ncloud_autoscaling.GetAutoScalingActivityLogListRequest()
        try:
            api_response = self.autoscaling_client.get_auto_scaling_activity_log_list(get_auto_scaling_activity_log_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_activity_log_list: %s\n" % e)

        return instance_list

    def List_Autoscaling_Configuration_Log(self):

        instance_list = []
        get_auto_scaling_configuration_log_list_request = ncloud_autoscaling.GetAutoScalingConfigurationLogListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_configuration_log_list(get_auto_scaling_configuration_log_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_configuration_log_list: %s\n" % e)

        return instance_list

    def List_Autoscaling_Group(self):

        instance_list = []
        get_auto_scaling_group_list_request = ncloud_autoscaling.GetAutoScalingGroupListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_group_list(get_auto_scaling_group_list_request)
            for instance in api_response.auto_scaling_group_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_group_list: %s\n" % e)

        return instance_list

    def List_Autoscaling_Policy(self):

        instance_list = []
        get_auto_scaling_policy_list_request = ncloud_autoscaling.GetAutoScalingPolicyListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_policy_list(get_auto_scaling_policy_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_policy_list: %s\n" % e)

        return instance_list

    def List_Launch_Configuration(self):

        instance_list = []
        get_launch_configuration_list_request = ncloud_autoscaling.GetLaunchConfigurationListRequest()

        try:
            api_response = self.autoscaling_client.get_launch_configuration_list(get_launch_configuration_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_launch_configuration_list: %s\n" % e)

        return instance_list

    def List_Scaling_Process_Type(self):

        instance_list = []
        get_scaling_process_type_list_request = ncloud_autoscaling.GetScalingProcessTypeListRequest()

        try:
            api_response = self.autoscaling_client.get_scaling_process_type_list(get_scaling_process_type_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_scaling_process_type_list: %s\n" % e)

        return instance_list

    def List_Scheduled_Action(self):

        instance_list = []
        get_scheduled_action_list_request = ncloud_autoscaling.GetScheduledActionListRequest()

        try:
            api_response = self.autoscaling_client.get_scheduled_action_list(get_scheduled_action_list_request)
            instance_list.append(api_response)

        except ApiException as e:
            print("Exception when calling V2Api->get_scheduled_action_list: %s\n" % e)

        return instance_list




