from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource



class Subnet(Model):
    subnet_no = StringType()
    vpc_no = StringType()
    zone_code = StringType()
    subnet_name = StringType()
    subnet = StringType()
    subnet_status = StringType()
    # create_date = StringType()
    subnet_type = StringType()
    usage_type = StringType()
    network_acl_no = StringType()


class Peering(Model):
    vpc_peering_instance_no = StringType()
    vpc_peering_name = StringType()
    last_modifiy_date = StringType()
    vpc_peering_instance_status = StringType()
    vpc_peering_instance_status_name = StringType()
    vpc_peering_instance_operation = StringType()
    source_vpc_no = StringType()
    source_vpc_name = StringType()
    source_vpc_ipv4_cidr_block = StringType()
    source_vpc_login_id = StringType()
    target_vpc_no = StringType()
    target_vpc_name = StringType()
    target_vpc_ipv4_cidr_block = StringType()
    target_vpc_login_id = StringType()
    vpc_peering_description = StringType()
    has_reverse_vpc_peering = BooleanType()
    is_between_accounts = BooleanType()
    reverse_vpc_peering_instance_no = StringType()


class RouteTable(Model):
    route_table_name = StringType()
    route_table_no = StringType()
    is_default = BooleanType()
    supported_subnet_type = StringType()
    route_table_status = StringType()
    route_table_description = StringType()

class NatGatewayInstance(Model):
    nat_gateway_instance_no = StringType()
    nat_gateway_name = StringType()
    public_ip = StringType()
    nat_gateway_instance_status = StringType()
    nat_gateway_instance_status_name = StringType()
    nat_gateway_instance_operation = StringType()
    create_date = StringType()
    nat_gateway_description = StringType()
    zone_code = StringType()

class NetworkAcl(Model):
    network_acl_no = StringType()
    network_acl_name = StringType()
    network_acl_status = StringType()
    network_acl_description = StringType()
    is_default = BooleanType()

class VPC(Model):
    vpc_no = StringType()
    vpc_name = StringType()
    ipv4_cidr_block = StringType()
    vpc_status = StringType()
    region_code = StringType()
    create_date = StringType()
    subnet_list = ListType(ModelType(Subnet))
    vpc_peering_list = ListType(ModelType(Peering))
    round_table_list = ListType(ModelType(RouteTable))
    nat_gateway_instance_list = ListType(ModelType(NatGatewayInstance))
    network_acl_list = ListType(ModelType(NetworkAcl))



    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/networking/networks/details/{self.name}?project={self.project}"
        }