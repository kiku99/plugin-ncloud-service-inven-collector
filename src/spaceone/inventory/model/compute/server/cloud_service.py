from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.compute.server.data import ServerInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField, \
    DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
Server Instance
'''
server_instance = ItemDynamicLayout.set_fields('Server Instance', fields=[
    TextDyField.data_source('Instance ID', 'data.compute.server_instance_no'),
    TextDyField.data_source('Instance Name', 'data.compute.server_name'),
    EnumDyField.data_source('Instance State', 'data.compute.server_instance_status', default_state={
        'safe': ['RUN'],
        'warning': ['INIT', 'CREAT', 'NSTOP'],
        'disable': ['FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'],
        'alert': ['TERMT']
    }),
    TextDyField.data_source('Instance Type', 'data.compute.server_instance_type'),
    TextDyField.data_source('Image', 'data.compute.server_image_name'),
    TextDyField.data_source('CPU Count', 'data.hardware.cpu_count'),
    TextDyField.data_source('Memory Size', 'data.hardware.memory_size'),
    TextDyField.data_source('Availability Zone', 'data.compute.zone'),
    TextDyField.data_source('Region', 'data.compute.region'),
    TextDyField.data_source('Public IP', 'data.ip.public_ip'),
    TextDyField.data_source('Private IP', 'data.ip.private_ip'),
    TextDyField.data_source('Port Forward External Port', 'data.port_forwarding_rules.port_forwarding_external_port'),
    TextDyField.data_source('Port Forward Internal Port', 'data.port_forwarding_rules.port_forwarding_internal_port'),
    TextDyField.data_source('Port Forward Public IP', 'data.port_forwarding_rules.port_forwarding_public_ip')
])

storage = ItemDynamicLayout.set_fields('Storage', fields=[
    TextDyField.data_source('Name', 'data.storage.storage_name'),
    SizeField.data_source('Size', 'data.storage.storage_size'),
    EnumDyField.data_source('Disk Type', 'data.storage.storage_diskType',
                            default_outline_badge=['NET', 'LOCAL']),
    EnumDyField.data_source('Disk Detail Type', 'data.storage.storage_disk_detail_type',
                            default_outline_badge=['HDD', 'SSD'])
])

login_key = ItemDynamicLayout.set_fields('Login Key', fields=[
    TextDyField.data_source('Name', 'data.login_key.key_name'),
    TextDyField.data_source('Finger Print', 'data.login_key.finger_print'),
    DateTimeDyField.data_source('Create Date', 'data.login_key.create_date')
])

server_instance_meta = CloudServiceMeta.set_layouts([server_instance, storage, login_key])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class ServerInstanceResource(ComputeResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(ServerInstance)
    _metadata = ModelType(CloudServiceMeta, default=server_instance_meta, serialized_name='metadata')


class ServerInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ServerInstanceResource)
