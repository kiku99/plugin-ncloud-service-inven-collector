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


class CloudDBConfig(Model):
    config_name = StringType()
    config_value = StringType()


class CloudDBConfigGroup(Model):
    config_group_no = StringType()
    config_group_type = StringType()
    config_group_name = StringType()


class AccessControlGroup(Model):
    access_control_group_name = StringType()
    access_control_group_description = StringType()
    create_date = StringType()


class CloudDBServerInstance(Model):
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
    add_block_storage_size = IntType()
    base_block_storage_size = IntType()
    db_kind_code = StringType()
    cpu_count = IntType()
    disk_type = StringType()
    infra_resource_type = StringType()
    memory_size = IntType()
    os_information = StringType()
    platform_type = StringType()
    product_code = StringType()
    product_description = StringType()
    product_name = StringType()
    product_type = StringType()


class CloudDBInstance(Model):
    cloud_db_instance_no = StringType()
    cloud_db_service_name = StringType()
    db_kind_code = StringType()
    cpu_count = IntType()
    data_storage_type = StringType()
    license_code = StringType()
    cloud_db_port = IntType()
    is_ha = BooleanType()
    backup_time = StringType()
    backup_file_retention_period = IntType()
    cloud_db_instance_status_name = StringType()
    collation = StringType()
    create_date = StringType()
    zone = StringType()
    region = StringType()
    cloud_db_config_list = ModelType(CloudDBConfig)
    cloud_db_config_group_list = ModelType(CloudDBConfigGroup)
    access_control_group_list = ModelType(AccessControlGroup)
    cloud_db_server_instance_list = ModelType(CloudDBServerInstance)





