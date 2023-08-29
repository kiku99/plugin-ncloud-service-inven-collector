from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


# common
# class getServerProductList(Model):
#     serverImageProductCode = StringType(20)
#     exclusionProductCode = StringType(20)
#     productCode = StringType(20)
#     generationCode = StringType(20)
#     regionNo = StringType()
#     zoneNo = StringType()
#
#
# class getServerImageProductList(Model):
#     exclusionProductCode = StringType(20)
#     productCode = StringType(20)
#     platformTypeCodeList = ListType()
#     blockStorageSize = IntType()
#     regionNO = StringType()
#     ingraResourceDetailTypeCode = StringType()
#
# # class getRaidList(Model):
#
# class getZoneList(Model):
#     regionNo = StringType()
#
# class getRegionList(Model):
#     regionNo = StringType()
#
# # class getInitScriptList(Model):
#
# class getLoginKeyList(Model):
#     keyName = StringType(30)
#     pageNo = IntType(2147483647)
#     pageSize = IntType(2147483647)


class AccessControlGroupList(Model):
    # 서버인스턴스 생성할때 사용자가 설정한 ACCESS Control Group을 넣어 방화벽기능 설정
    accessControlGroupConfigurationNoList = ListType(IntType())
    isDefaultGroup = BooleanType
    accessControlGroupName = StringType()
    pageNo = IntType()
    pageSize = IntType()


# class getAccessControlGroupServerInstanceList(Model): # 접근제어그룹설정 번호로 등록된 서버 인스턴스 리스트들 조회
#     accessControlGroupConfigurationNo = StringType()


# class getAccessControlRuleList(Model):#접근제어규칙리스트초회
#     accessControlGroupConfigurationNo = StringType()

# disk
class ServerInstanceList(Model):  # 서버 인스턴스 리스트 조회(페이징처리)
    serverInstanceNoList = ListType(IntType())
    searchFilterName = StringType()
    searchFilterValue = StringType()
    pageNo = IntType()
    pageSize = IntType()
    serverInstanceStatusCode = StringType()
    regionNo = StringType()
    zoneNo = StringType()
    baseBlockStorageDiskTypeCode = StringType()
    baseBlockStorageDiskDetailTypeCode = StringType()
    sortedBy = StringType()
    sortingOrder = StringType()


# class recreateServerInstances(Model) : #서버인스턴스 재생성(베어메탈상품 전용)
#     serverInstanceNo = StringType()
#     serverInstanceName = StringType()
#     serverImageProductCode = StringType()
#     userData = StringType(21847)
#     instanceTagListKey = ListType()
#     instanceTagListValue = ListType()

# class terminateServerInstances(Model) : #서버 인스턴스 반납?
#     serverInstaceNoList = ListType()

class MemberServerImage(Model):  # 서버이미지 생성
    memberServerImageName = StringType()
    memberServerImageDescription = StringType()
    serverInstanceNo = StringType()


class PublicIpTargetServerInstanceList(Model):  # IP할당 가능 서버 인스턴스 조회
    regionNo = StringType()
    zoneNo = StringType()


class PublicIpInstance(Model):
    serverInstanceNo = StringType()
    publicIpDescription = StringType()
    regionNo = StringType()
    zoneNo = StringType()


class PortForwardingRuleList(Model):
    regionNo = StringType()
    zoneNo = StringType()


class PublicIpInstanceList(Model):  # 공인 IP 인스턴스 리스트를 조회
    isAssociated = BooleanType()
    publicIpInstanceNoList = StringType()
    publicIpList = ListType(StringType, default=[])
    searchFilterName = StringType()
    searchFilterValue = StringType()
    regionNo = StringType()
    zoneNo = StringType()
    pageNo = IntType()
    pageSize = IntType()
    sortedBy = StringType()
    sortingOrder = StringType()


class PortForwardingRules(Model):  # 포트포워딩룰
    portForwardingConfigurationNo = StringType()
    portForwardingRuleListInstanceNo = StringType()
    portForwardingRule_portForwardingExternalPort = StringType()
    portForwardingRule_portForwardingInternalPort = StringType()


class Labels(Model):
    key = StringType()
    value = StringType()


class Tags(Model):
    instanceNoList = ListType(StringType, default=[])
    instanceTag_key = StringType()
    instanceTag_Value = StringType()


class InstanceTagList(Model):
    instanceNoList = ListType(StringType, default=[])
    tagKeyList = ListType(StringType, default=[])
    tagValueList = ListType(StringType, default=[])
    pageNo = IntType()
    pageSize = IntType()


class ProtectServerTermination(Model):  # 서버반납보호여부
    serverInstanceNo = StringType()
    isProtectServerTermination = BooleanType()


class InterruptServerInstance(Model):
    serverInstanceNo = StringType()


class Description(Model):
    description = StringType()


class AccessPolicy(Model):
    service_account = StringType()
    display_name = StringType()
    scopes = ListType(ModelType(Description))


# InstanceGroup
class InstanceGroup(Model):
    id = StringType()
    self_link = StringType()
    name = StringType()
    instance_template_name = StringType()


class AutoScaler(Model):
    id = StringType()
    self_link = StringType()
    name = StringType()
    instance_group = ModelType(InstanceGroup, serialize_when_none=False)


class Scheduling(Model):
    on_host_maintenance = StringType(default="MIGRATE")
    automatic_restart = BooleanType(default=True)
    preemptible = BooleanType(default=False)


class Key(Model):
    user_name = StringType()
    ssh_key = StringType()
    display_name = StringType()


class SSHKey(Model):
    block_project_ssh_keys = StringType()
    ssh_keys = ListType(ModelType(Key))


# class NaverCloud(Model):
#     self_link = StringType()
#     fingerprint = StringType()
#     reservation_affinity = StringType(default="ANY_RESERVATION")
#     deletion_protection = BooleanType(default=False)
#     scheduling = ModelType(Scheduling)
#     tags = ListType(ModelType(Tags))
#     labels = ListType(ModelType(Labels), default=[])
#     ssh_keys = ModelType(SSHKey)
#     service_accounts = ListType(ModelType(AccessPolicy), default=[])
#     is_managed_instance = BooleanType(default=False)

# disk
# class DiskTags(Model):
#     disk_id = StringType(serialize_when_none=False)
#     disk_name = StringType(serialize_when_none=False)
#     description = StringType(serialize_when_none=False)
#     zone = StringType(serialize_when_none=False)
#     disk_type = StringType(choices=('local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard'), serialize_when_none=False)
#     encrypted = BooleanType(default=True)
#     read_iops = FloatType(serialize_when_none=False)
#     write_iops = FloatType(serialize_when_none=False)
#     read_throughput = FloatType(serialize_when_none=False)
#     write_throughput = FloatType(serialize_when_none=False)
#     labels = ListType(ModelType(Labels), default=[], serialize_when_none=False)


# class Disk(Model):
#     device_index = IntType()
#     device = StringType(default="")
#     disk_type = StringType(default="disk")
#     size = FloatType()
#     tags = ModelType(DiskTags, default={})


# loadbalancing = load_balancer
class LoadBalancer(Model):
    type = StringType(choices=('HTTP', 'TCP', 'UDP'))
    name = StringType()
    dns = StringType(default="")
    port = ListType(IntType())
    protocol = ListType(StringType())
    scheme = StringType(choices=('EXTERNAL', 'INTERNAL'))
    tags = DictType(StringType, default={})


# nic
class NIC(Model):
    publicIp = StringType()
    privateIp = StringType()
    portForwardingPublicIp = StringType()
    portForwardingExternalPort = IntType()
    portForwardingInternalPort = IntType()


# Firewallf
class SecurityGroup(Model):
    priority = IntType(serialize_when_none=False)
    protocol = StringType()
    remote = StringType()  # mimic
    remote_id = StringType(serialize_when_none=False)  # filter value
    remote_cidr = StringType(serialize_when_none=False)  # cidr
    security_group_name = StringType(default="")
    port_range_min = IntType(serialize_when_none=False)
    port_range_max = IntType(serialize_when_none=False)
    security_group_id = StringType()
    description = StringType(default="")
    direction = StringType(choices=("inbound", "outbound"))
    port = StringType(serialize_when_none=False)
    action = StringType(choices=('allow', 'deny'))


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


class GPU(Model):
    gpu_machine_type = StringType(serialize_when_none=False)
    gpu_count = IntType(serialize_when_none=False)


# class Display(Model):
#     gpus = ListType(StringType, default=[])
#     has_gpu = BooleanType(default=False)

class Storage(Model):  # 블록스토리지인스턴스
    storageName = StringType()
    storageSize = LongType()
    storageDescription = StringType()
    storageDiskType = StringType(choices=('LOCAL', 'NET'))
    storageDiskDetailType = StringType(choices=('LOCAL', 'NET'))


class OS(Model):
    platformType = StringType(choices=('LNX32', 'WIN64'))


class Compute(Model):
    serverInstanceNo = StringType()
    serverName = StringType()
    serverDescription = StringType()
    serverImageName = StringType()
    serverInstanceStatus = StringType(
        choices=('INIT', 'CREAT', 'RUN', 'NSTOP', 'TERMT', 'FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'))
    serverInstanceOperation = StringType(choices=(
        'START', 'SHTDN', 'RESTA', 'TERMT', 'NULL', 'MIGRA', 'COPY', 'SETUP', 'HREST', 'HSHTD', 'CHNG', 'CREAT'))
    serverInstanceStatusName = StringType()
    createDate = DateTimeType()
    uptime = DateTimeType()
    serverImageProductCode = StringType()
    serverProductCode = StringType()
    serverInstanceType = StringType(choices=('LOCAL', 'NET'))
    zone = StringType(serialize_when_none=False)
    region = StringType(serialize_when_none=False)


############################# 얘가 제일 중요 #####################################
class ServerInstance(Model):
    compute = ModelType(Compute)
    os = ModelType(OS)
    nics = ListType(ModelType(NIC))
    storage = ModelType(Storage)
    cpuCount = IntType()
    memorySize = LongType()
    loginKeyName = StringType()
    userData = StringType()
    accessControlGroupList = ListType(StringType, default=[])
    blockDevicePartitionList = ListType(StringType, default=[])
