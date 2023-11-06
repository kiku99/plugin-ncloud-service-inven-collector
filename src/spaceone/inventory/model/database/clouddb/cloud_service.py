from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.database.clouddb.data import Product, Clouddbinstance
from spaceone.inventory.model.database.clouddb.data import CloudDBInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
CloudDB
'''
cloud_db_instance = ItemDynamicLayout.set_fields('CloudDB Instance', fields=[
    TextDyField.data_source('DB Service Name', 'data.name'),
    TextDyField.data_source('Backup File Retention Period', 'data.backup_file_retention_period'),
    EnumDyField.data_source('State', 'data.cloud_db_instance_status_name', default_state={
        'safe': ['running'],
        'disable': ['deleting', 'creating', 'pending', 'recovering', 'restarting', 'reinstalling'],
        'alert': ['deleted']
    }),
    TextDyField.data_source('Backup Time', 'data.backup_time'),
    TextDyField.data_source('CPU Count', 'data.cpu_count'),
    TextDyField.data_source('Data Storage Type', 'data.data_storage_type'),
    TextDyField.data_source('Instance Port', 'data.cloud_db_port'),
    TextDyField.data_source('DB Type', 'data.db_kind_code'),
    TextDyField.data_source('DB License', 'data.license_code'),
    TextDyField.data_source('DB Engine Version', 'data.engine_version'),

])

access_control_group = ItemDynamicLayout.set_fields('Access Control Group', fields=[
    TextDyField.data_source('Name', 'data.access_control_group_list.access_control_group_name'),
    TextDyField.data_source('Lanched', 'data.access_control_group_list.create_date'),
    ListDyField.data_source('Description', 'data.access_control_group_list.access_control_group_description'),

])

cloud_db_server = ItemDynamicLayout.set_fields('CloudDB Server Instance', fields=[
    TextDyField.data_source('Name', 'data.cloud_db_server_instance_list.cloud_db_server_name'),
    TextDyField.data_source('DB Role', 'data.cloud_db_server_instance_list.cloud_db_server_role'),
    TextDyField.data_source('Lanched', 'data.cloud_db_server_instance_list.create_date'),
    TextDyField.data_source('Private DNS Name', 'data.cloud_db_server_instance_list.private_dns_name'),
    TextDyField.data_source('Public DNS Name', 'data.cloud_db_server_instance_list.public_dns_name'),
    TextDyField.data_source('uptime', 'data.cloud_db_server_instance_list.uptime'),
    SizeField.data_source('Data StorageSize', 'data.cloud_db_server_instance_list.data_storage_size'),
    SizeField.data_source('Used Data StorageSize', 'data.cloud_db_server_instance_list.used_data_storage_size'),
    EnumDyField.data_source('State', 'data.cloud_db_server_instance_list.cloud_db_instance_status_name', default_state={
        'safe': ['running'],
        'disable': ['deleting', 'creating', 'pending', 'recovering', 'restarting', 'reinstalling'],
        'alert': ['deleted'],
    })
])

cloud_db_instance_meta = CloudServiceMeta.set_layouts([cloud_db_instance, access_control_group, cloud_db_server])


class CloudDBInstancetResource(CloudServiceResource):
    cloud_service_group = StringType(default='Database')


class CloudDBResource(CloudDBInstancetResource):
    cloud_service_type = StringType(default='CloudDB')
    data = ModelType(CloudDBInstance)
    _metadata = ModelType(CloudServiceMeta, default=cloud_db_instance_meta, serialized_name='metadata')


class CloudDBResponse(CloudServiceResponse):
    resource = PolyModelType(CloudDBResource)