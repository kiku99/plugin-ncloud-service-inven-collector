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
    portForwardingConfigurationNo = StringType()
    portForwardingRuleListInstanceNo = StringType()
    portForwardingRule_portForwardingExternalPort = StringType()
    portForwardingRule_portForwardingInternalPort = StringType()


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
    nic_type = StringType(default="Virtual")  # 확인 필요
    ip_addresses = ListType(StringType())  # 확인필요 (accessConfig)
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
    cpu_machine_type = StringType(serialize_when_none=False)
    cpuCount = IntType()
    gpu_machine_type = StringType(serialize_when_none=False)
    gpu_count = IntType(serialize_when_none=False)
    memorySize = LongType()


class Storage(Model):  # 블록스토리지인스턴스
    storageName = StringType()
    storageSize = LongType()
    storageDescription = StringType()
    storageDiskType = StringType(choices=('LOCAL', 'NET'))
    storageDiskDetailType = StringType(choices=('LOCAL', 'NET'))
    #     read_iops = FloatType(serialize_when_none=False)
    #     write_iops = FloatType(serialize_when_none=False)
    #     read_throughput = FloatType(serialize_when_none=False)
    #     write_throughput = FloatType(serialize_when_none=False)


class Compute(Model):
    serverImageName = StringType()
    serverInstanceStatus = StringType(
        choices=('INIT', 'CREAT', 'RUN', 'NSTOP', 'TERMT', 'FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'))
    serverInstanceOperation = StringType(choices=(
        'START', 'SHTDN', 'RESTA', 'TERMT', 'NULL', 'MIGRA', 'COPY', 'SETUP', 'HREST', 'HSHTD', 'CHNG', 'CREAT'))
    serverInstanceStatusName = StringType()
    platformType = StringType(choices=('LNX32', 'WIN64'))
    createDate = DateTimeType()
    uptime = DateTimeType()
    serverImageProductCode = StringType()
    serverProductCode = StringType()
    serverInstanceType = StringType(choices=('MICRO', 'COMPT', 'STAND', 'GPU', 'LDISK', 'CHADP', 'BM', 'VDS'))
    zone = StringType(serialize_when_none=False)
    region = StringType(serialize_when_none=False)
    portForwardingRules = ModelType(PortForwardingRules)


class LoginKey(Model):
    fingerprint = StringType()
    keyName = StringType()
    createData = DateTimeType()


class NaverCloud(Model):
    loginKey = ModelType(LoginKey)
    memberNo = StringType()


class ServerInstance(Model):
    serverInstanceNo = StringType()
    serverInstanceName = StringType()
    serverInstanceDescription = StringType()
    compute = ModelType(Compute)
    nics = ListType(ModelType(NIC))
    storage = ModelType(Storage)
    hardware = ModelType(Hardware)
    vpc = ModelType(VPC)
    subnet = ModelType(Subnet)
    naverCloud = ModelType(NaverCloud)
    tag = ModelType(InstanceTag)
    protectServerTermination = ModelType(ProtectServerTermination)
    accessControlGroupList = ListType(ModelType(AccessControlGroupList))


class ServerInstanceList(Model):  # 서버 인스턴스 리스트 조회(페이징처리)
    serverInstance = ListType(ModelType(ServerInstance))
    serverInstanceNoList = ListType(StringType())
    searchFilterName = StringType()
    searchFilterValue = StringType()
    pageNo = IntType()
    pageSize = IntType()
    serverInstanceStatusCode = StringType()
    regionNo = StringType()
    zoneNo = StringType()
    sortedBy = StringType()
    sortingOrder = StringType()
