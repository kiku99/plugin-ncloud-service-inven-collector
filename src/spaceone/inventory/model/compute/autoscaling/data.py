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
    activityNo = StringType()
    # autoScalingGroupName = StringType()
    status = StringType()
    statusMessage = StringType()
    # actionCause = StringType()
    description = StringType()
    details = StringType()
    startTime = DateTimeType()
    endTime = DateTimeType()


class AdjustmentType(Model):
    adjustment_type = StringType()


class ConfigurationLog(Model):
    configurationNo = StringType()
    configurationActionName = StringType()
    # parameters = StringType()
    launchConfigurationName = StringType()
    # autoScalingGroupName = StringType()
    scheduledActionName = StringType()
    settingTime = DateTimeType()


class ScalingPolicy(Model):
    policyName = StringType()
    autoScalingGroupName = StringType()
    adjustmentType = StringType()
    scalingAdjustment = IntType()
    cooldown = IntType()
    minAdjustmentStep = IntType()


class AccessControlGroup(Model):
    accessControlGroupConfigurationNo = StringType()
    accessControlGroupDescription = StringType()
    accessControlGroupName = StringType()
    # createDate = DateTimeType()
    isDefaultGroup = StringType()


class LaunchConfiguration(Model):
    launchConfigurationName = StringType()
    # launchConfigurationNo = StringType()
    # serverImageProductCode = StringType()
    # serverProductCode = StringType()
    # memberServerImageNo = StringType()
    loginKeyName = StringType()
    # createDate = DateTimeType()
    # userData = StringType(default=None)
    # initScriptNo = StringType(default=None)
    accessControlGroupList = ListType(ModelType(AccessControlGroup))


class Process(Model):
    process = StringType()


class ScheduledUpdateGroupAction(Model):
    autoScalingGroupName = StringType()
    scheduledActionName = StringType()
    desiredCapacity = IntType()
    minSize = IntType()
    maxSize = IntType()
    startTime = DateTimeType()
    endTime = DateTimeType(default=None)
    recurrenceInKST = DateTimeType(default=None)


class Zone(Model):
    zoneDescription = StringType()
    zoneName = StringType()
    zoneNo = StringType()


class AutoScalingGroup(Model):
    # autoScalingGroupName = StringType()
    # autoScalingGroupNo = StringType()
    # launchConfigurationName = StringType()
    # launchConfigurationNo = StringType()
    desiredCapacity = IntType()
    minSize = IntType()
    maxSize = IntType()
    defaultCooldown = IntType()
    # loadBalancerInstanceSummaryList = ListType(StringType())
    healthCheckGracePeriod = IntType()
    healthCheckType = StringType()
    # createDate = DateTimeType()
    # inAutoScalingGroupServerInstanceList = ListType(StringType())
    # suspendedProcessList = ListType(StringType())
    zoneList = ListType(ModelType(Zone))

    activityLogList = ListType(ModelType(ActivityLog))
    # adjustmentType = ModelType(AdjustmentType)
    configurationLogList = ListType(ModelType(ConfigurationLog))
    # scalingPolicy = ModelType(ScalingPolicy)
    launchConfigurationList = ListType(ModelType(LaunchConfiguration))
    # process = ModelType(Process)
    # scheduledUpdateGroupAction = ModelType(ScheduledUpdateGroupAction)
