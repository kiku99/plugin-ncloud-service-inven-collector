from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


# class AutoScalingGroup(Model):
#     autoScalingGroupName = StringType()
#     autoScalingGroupNo = StringType()
#     launchConfigurationName = StringType()
#     launchConfigurationNo = StringType()
#     desiredCapacity = IntType()
#     minSize = IntType()
#     maxSize = IntType()
#     defaultCooldown = IntType()
#     loadBalancerInstanceSummaryList = ListType(StringType())
#     healthCheckGracePeriod = IntType()
#     healthCheckType = StringType()
#     createDate = DateTimeType()
#     inAutoScalingGroupServerInstanceList = ListType(StringType())
#     suspendedProcessList = ListType(StringType())
#     zoneList = ListType(StringType())


class ActivityLog(Model):
    activity_no = StringType()
    # autoScalingGroupName = StringType()
    status = StringType()
    status_message = StringType()
    # actionCause = StringType()
    description = StringType()
    details = StringType()
    start_time = DateTimeType()
    end_time = DateTimeType()


class AdjustmentType(Model):
    adjustment_type = StringType()


class ConfigurationLog(Model):
    configuration_no = StringType()
    configuration_action_name = StringType()
    # parameters = StringType()
    launch_configuration_name = StringType()
    # autoScalingGroupName = StringType()
    scheduled_action_name = StringType()
    setting_time = DateTimeType()


class ScalingPolicy(Model):
    policy_name = StringType()
    auto_scaling_group_name = StringType()
    adjustment_type = StringType()
    scaling_adjustment = IntType()
    cooldown = IntType()
    min_adjustment_step = IntType()


class AccessControlGroup(Model):
    access_control_group_configuration_no = StringType()
    access_control_group_description = StringType()
    access_control_group_name = StringType()
    # createDate = DateTimeType()
    is_default_group = StringType()


class LaunchConfiguration(Model):
    launch_configuration_name = StringType()
    # launchConfigurationNo = StringType()
    # serverImageProductCode = StringType()
    # serverProductCode = StringType()
    # memberServerImageNo = StringType()
    login_key_name = StringType()
    # createDate = DateTimeType()
    # userData = StringType(default=None)
    # initScriptNo = StringType(default=None)
    access_control_group_list = ListType(ModelType(AccessControlGroup))


class Process(Model):
    process = StringType()


class ScheduledUpdateGroupAction(Model):
    auto_scaling_group_name = StringType()
    scheduled_action_name = StringType()
    desired_capacity = IntType()
    min_size = IntType()
    max_size = IntType()
    start_time = DateTimeType()
    end_time = DateTimeType(default=None)
    recurrence_in_kst = DateTimeType(default=None)


class Zone(Model):
    zone_description = StringType()
    zone_name = StringType()
    zone_no = StringType()


class AutoScalingGroup(Model):
    # autoScalingGroupName = StringType()
    # autoScalingGroupNo = StringType()
    # launchConfigurationName = StringType()
    # launchConfigurationNo = StringType()
    desired_capacity = IntType()
    min_size = IntType()
    max_size = IntType()
    default_cooldown = IntType()
    # loadBalancerInstanceSummaryList = ListType(StringType())
    health_check_grace_period = IntType()
    health_check_type = StringType()
    # createDate = DateTimeType()
    # inAutoScalingGroupServerInstanceList = ListType(StringType())
    # suspendedProcessList = ListType(StringType())
    zone_list = ListType(ModelType(Zone))

    activity_log_list = ListType(ModelType(ActivityLog))
    # adjustmentType = ModelType(AdjustmentType)
    configuration_log_list = ListType(ModelType(ConfigurationLog))
    # scalingPolicy = ModelType(ScalingPolicy)
    launch_configuration_list = ListType(ModelType(LaunchConfiguration))
    # process = ModelType(Process)
    # scheduledUpdateGroupAction = ModelType(ScheduledUpdateGroupAction)
