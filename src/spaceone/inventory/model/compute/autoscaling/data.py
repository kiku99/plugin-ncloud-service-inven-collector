from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class AutoScalingGroup(Model):
    autoScalingGroupName = StringType()
    autoScalingGroupNo = StringType()
    launchConfigurationName = StringType()
    launchConfigurationNo = StringType()
    desiredCapacity = IntType()
    minSize = IntType()
    maxSize = IntType()
    defaultCooldown = IntType()
    loadBalancerInstanceSummaryList = ListType(StringType())
    healthCheckGracePeriod = IntType()
    healthCheckType = StringType()
    createDate = DateTimeType()
    inAutoScalingGroupServerInstanceList = ListType(StringType())
    suspendedProcessList = ListType(StringType())
    zoneList = ListType(StringType())


class ActivityLog(Model):
    activityNo = StringType()
    autoScalingGroupName = StringType()
    status = StringType()
    statusMessage = StringType()
    actionCause = StringType()
    description = StringType()
    details = StringType()
    startTime = DateTimeType()
    endTime = DateTimeType()


class AdjustmentType(Model):
    adjustment_type = StringType()


class ConfigurationLog(Model):
    configurationNo = StringType()
    configurationActionName = StringType()
    parameters = StringType()
    launchConfigurationName = StringType()
    autoScalingGroupName = StringType()
    scheduledActionName = StringType()
    settingTime = DateTimeType()


class ScalingPolicy(Model):
    policyName = StringType()
    autoScalingGroupName = StringType()
    adjustmentType = StringType()
    scalingAdjustment = IntType()
    cooldown = IntType()
    minAdjustmentStep = IntType()


class LaunchConfiguration(Model):
    launchConfigurationName = StringType()
    launchConfigurationNo = StringType()
    serverImageProductCode = StringType()
    serverProductCode = StringType()
    memberServerImageNo = StringType()
    loginKeyName = StringType()
    createDate = DateTimeType()
    userData = StringType(default=None)
    initScriptNo = StringType(default=None)
    accessControlGroupList = ListType(StringType(), default=None)


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
