from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class AccessControlGroup(Model):
    access_control_group_configuration_no = StringType()
    access_control_group_name = StringType()
    access_control_group_description = StringType()
    is_default_group = BooleanType()
    create_data = DateTimeType()


class AccessControlGroupList(Model):
    # 서버인스턴스 생성할때 사용자가 설정한 ACCESS Control Group을 넣어 방화벽 기능 설정
    access_control_group = ModelType(AccessControlGroup)
    access_control_group_configuration_no_list = ListType(StringType())
    is_default_group = BooleanType()
    access_control_group_name = StringType()
    page_no = IntType()
    page_size = IntType()


class PortForwardingRules(Model):  # 포트포워딩룰
    port_forwarding_external_port = StringType(default=None)
    port_forwarding_internal_port = StringType(default=None)
    port_forwarding_public_ip = StringType()


class InstanceTag(Model):
    instance_no = StringType()
    instance_type = StringType()
    tag_key = StringType()
    tag_value = StringType()


class InstanceTagList(Model):
    instance_tag = ModelType(InstanceTag)
    instance_no_list = ListType(StringType, default=[])
    tag_key_list = ListType(StringType, default=[])
    tag_value_list = ListType(StringType, default=[])
    page_no = IntType()
    page_size = IntType()


class ProtectServerTermination(Model):  # 서버반납보호여부
    server_instance_no = StringType()
    is_protect_server_termination = BooleanType()


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
    cpu_count = IntType()
    memory_size = IntType()


# 블록스토리지인스턴스
class Storage(Model):
    storage_name = StringType()
    storage_size = LongType()
    storage_description = StringType()
    storage_diskType = StringType()
    storage_disk_detail_type = StringType()


class Compute(Model):
    server_name = StringType()
    server_image_name = StringType()
    server_instance_status = StringType(choices=(
        'INIT', 'CREAT', 'RUN', 'NSTOP', 'TERMT', 'FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'
    ))
    server_instance_operation = StringType()
    server_instance_status_name = StringType()
    platform_type = StringType()
    create_date = DateTimeType()
    uptime = DateTimeType()
    server_image_product_code = StringType()
    server_product_code = StringType()
    server_instance_type = StringType(choices=(
        'MICRO', 'COMPT', 'STAND', 'GPU', 'LDISK', 'CHADP', 'BM', 'VDS'
    ))
    zone = StringType()
    region = StringType()


class LoginKey(Model):
    finger_print = StringType()
    key_name = StringType()
    create_date = DateTimeType()


class IP(Model):
    private_ip = StringType()
    public_ip = StringType()


class ServerInstance(Model):
    compute = ModelType(Compute)
    port_forwarding_rules = ModelType(PortForwardingRules)
    ip = ModelType(IP)
    storage = ModelType(Storage)
    hardware = ModelType(Hardware)
    login_Key = ModelType(LoginKey)
