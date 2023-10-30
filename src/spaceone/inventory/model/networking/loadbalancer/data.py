from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType
from spaceone.inventory.libs.schema.cloud_service import BaseResource


class Zone(Model):
    zone_no = StringType()
    zone_name = StringType()
    zone_description = StringType()

class Region(Model):
    region_no = StringType()
    region_code = StringType()
    region_name = StringType()

class sslCertificate(Model):
    certificate_name = StringType()
    private_key = StringType()
    public_key_certificate = StringType()
    certificate_chain = StringType()

class AccessControlGroup(Model):
    access_control_group_configuration_no = StringType()
    access_control_group_name = StringType()
    access_control_group_description = StringType()
    is_default = BooleanType()
    create_date = StringType()

class ServerInstance(Model):
    server_instance_no = StringType()
    server_name = StringType()
    server_description = StringType()
    cpu_count = IntType()
    memory_size = IntType()
    base_block_storage_size = IntType()
    platform_type = StringType() #common
    login_key_name = StringType()
    is_fee_charging_monitoring = BooleanType()
    public_ip = StringType()
    private_ip = StringType()
    server_image_name = StringType()
    server_instance_status = StringType() #common
    server_instance_operation = StringType() #common
    server_instance_status_name = StringType()
    create_date = StringType()
    uptime = StringType()
    server_image_product_code = StringType()
    server_product_code = StringType()
    is_protect_server_termination = BooleanType()
    port_forwarding_public_ip = StringType()
    port_forwarding_external_port = IntType()
    port_forwarding_internal_port = IntType()
    zone = ModelType(Zone)
    region = ModelType(Region)
    base_block_storage_disk_type = StringType() #common
    base_block_storage_disk_detail_type = StringType() #common
    internet_line_type = StringType() #common
    user_data = StringType()
    access_control_group_list = ListType(ModelType(AccessControlGroup))

class ServerHealthCheckStatus(Model):
    protocol_type = StringType() #common
    load_balancer_port = IntType()
    server_port = IntType()
    l7_health_check_path = StringType()
    proxy_protocol_use_yn = StringType()
    server_status = BooleanType()

class LoadBalancerRule(Model):
    protocol_type = StringType() #common
    load_balancer_port = IntType()
    server_port = IntType()
    l7_health_check_path = StringType()
    certificate_name = StringType()
    proxy_protocol_use_yn = StringType()

class LoadBalancedServerInstance(Model):
    server_instance = ModelType(ServerInstance)
    server_health_check_status_list = ListType(ModelType(ServerHealthCheckStatus))
class LoadBalancerInstance(Model):
    load_balancer_instance_no = StringType()
    virtual_ip = StringType()
    load_balancer_name = StringType()
    load_balancer_algorithm_type = StringType() #common
    load_balancer_description = StringType()
    create_date = StringType()
    domain_name = StringType()
    internet_line_type = StringType() #common
    load_balancer_instance_status_name = StringType()
    load_balancer_instance_status = StringType() #common
    load_balancer_instance_operation = StringType() #common
    network_usage_type = StringType() #common
    is_http_keep_alive = StringType()
    connection_timeout = StringType()
    certificate_name = StringType()
    load_balancer_rule_list = ListType(ModelType(LoadBalancerRule))
    load_balanced_server_instance_list = ListType(ModelType(LoadBalancedServerInstance))

    def reference(self, refer_link):
        return {
            "resource_id": self.self_link,
            "external_link": refer_link
        }
