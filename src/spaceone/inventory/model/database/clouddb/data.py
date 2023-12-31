from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class BackupFile(Model):
    host_name = StringType()
    file_name = StringType()
    database_name = StringType()
    first_lsn = StringType()
    last_lsn = StringType()
    backup_type = StringType()
    backup_start_time = StringType()
    backup_end_time = StringType()


class DmsFile(Model):
    file_length = IntType()
    last_write_time = StringType()
    file_name = StringType()

class Region(Model):
    region_no = StringType()
    region_code = StringType()
    region_name = StringType()

class Zone(Model):
    zone_description = StringType()
    zone_name = StringType()
    zone_no = StringType()


class CloudDBConfig(Model):
    config_name = StringType()
    config_value = StringType()


class CloudDBConfigGroup(Model):
    config_group_no = StringType()
    config_group_type = StringType()
    config_group_name = StringType()


class AccessControlGroup(Model):
    access_control_group_name = StringType()
    access_control_group_configuration_no = StringType()
    access_control_group_description = StringType()
    create_date = StringType()


class CloudDBServerInstance(Model):
    cloud_db_server_instance_no = StringType()
    cloud_db_server_instance_status_name = StringType()
    cloud_db_server_name = StringType()
    cloud_db_server_role = StringType()
    private_dns_name = StringType()
    public_dns_name = StringType()
    data_storage_size = IntType()
    used_data_storage_size = IntType()
    create_date = StringType()
    uptime = StringType()


class Product(Model):
    base_block_storage_size = IntType()
    #dbKindCode = StringType()
    cpu_count = IntType()
    #disk_type = StringType()
    infra_resource_type = StringType()
    memory_size = IntType()
    #os_information = StringType()
   # platform_type = StringType()
    product_code = StringType()
    product_description = StringType()
    product_name = StringType()
    product_type = StringType()




class CloudDBInstance(Model):
    cloud_db_instance_no = StringType()
    cloud_db_service_name = StringType()
    db_kind_code = StringType()
    cpu_count = IntType()
    engine_version = StringType()
    data_storage_type = StringType()
    license_code = StringType()
    cloud_db_port = StringType()
    is_ha = BooleanType()
    backup_time = StringType()
    backup_file_retention_period = IntType()
    cloud_db_instance_status_name = StringType()
    #collation = StringType()
    #create_date = StringType()
    zone_list = ListType(ModelType(Zone))
    region_list = ListType(ModelType(Region))
    #cloud_db_config_list = ModelType(CloudDBConfig)
    #cloud_db_config_group_list = ModelType(CloudDBConfigGroup)
    access_control_group_list = ListType(ModelType(AccessControlGroup))
    cloud_db_server_instance_list = ListType(ModelType(CloudDBServerInstance))


class Clouddbinstance(Model):
    productGroup = ModelType(Product)
    #configGroupList = ListType(ModelType(CloudDBConfigGroup))









