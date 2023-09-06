from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class AccessControlGroup(Model):
    accessControlGroupConfigurationNo = StringType()
    accessControlGroupName = StringType()
    accessControlGroupDescription = StringType()
    isDefaultGroup = BooleanType()
    createData = DateTimeType()


class AccessControlGroupList(Model):
    # 서버인스턴스 생성할때 사용자가 설정한 ACCESS Control Group을 넣어 방화벽 기능 설정
    accessControlGroup = ModelType(AccessControlGroup)
    accessControlGroupConfigurationNoList = ListType(StringType())
    isDefaultGroup = BooleanType
    accessControlGroupName = StringType()
    pageNo = IntType()
    pageSize = IntType()


class PortForwardingRules(Model):  # 포트포워딩룰
    port_forwarding_external_port = StringType(default=None)
    port_forwarding_internal_port = StringType(default=None)
    port_forwarding_public_ip = StringType()


class InstanceTag(Model):
    instanceNo = StringType()
    instanceType = StringType()
    tagKey = StringType()
    tagValue = StringType()


class InstanceTagList(Model):
    instanceTag = ModelType(InstanceTag)
    instanceNoList = ListType(StringType, default=[])
    tagKeyList = ListType(StringType, default=[])
    tagValueList = ListType(StringType, default=[])
    pageNo = IntType()
    pageSize = IntType()


class ProtectServerTermination(Model):  # 서버반납보호여부
    serverInstanceNo = StringType()
    isProtectServerTermination = BooleanType()


# nic
class NIC(Model):
    device_index = IntType()
    device = StringType(default="")
    cidr = StringType()
    nic_type = StringType(default="Virtual")
    ip_addresses = ListType(StringType())
    mac_address = StringType(default="")
    public_ip_address = StringType()
    tags = DictType(StringType, default={})


# vpc
class VPC(Model):
    vpc_id = StringType()
    vpc_name = StringType(default="")
    description = StringType(default="")
    self_link = StringType(default="")


# subnet
class Subnet(Model):
    subnet_id = StringType()
    cidr = StringType()
    subnet_name = StringType()
    gateway_address = StringType()
    vpc = ModelType(VPC)
    self_link = StringType()


class Hardware(Model):
    cpuCount = IntType()
    memorySize = IntType()


class Storage(Model):  # 블록스토리지인스턴스
    storageName = StringType()
    storageSize = LongType()
    storageDescription = StringType()
    storageDiskType = StringType()
    storageDiskDetailType = StringType()


class Compute(Model):
    serverName = StringType()
    serverImageName = StringType()
    serverInstanceStatus = StringType()
    serverInstanceOperation = StringType()
    serverInstanceStatusName = StringType()
    platformType = StringType()
    createDate = DateTimeType()
    uptime = DateTimeType()
    serverImageProductCode = StringType()
    serverProductCode = StringType()
    serverInstanceType = StringType()
    zone = StringType()
    region = StringType()


class LoginKey(Model):
    fingerPrint = StringType()
    keyName = StringType()
    createDate = DateTimeType()


class IP(Model):
    privateIP = StringType()
    publicIP = StringType()


class ServerInstance(Model):
    compute = ModelType(Compute)
    portForwardingRules = ModelType(PortForwardingRules)
    ip = ModelType(IP)
    storage = ModelType(Storage)
    hardware = ModelType(Hardware)
    loginKey = ModelType(LoginKey)
