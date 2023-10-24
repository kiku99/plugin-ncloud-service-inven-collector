from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.compute.server.data import ServerInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
Server Instance
'''
server_instance = ItemDynamicLayout.set_fields('Server Instance', fields=[
    TextDyField.data_source('Account', 'data.compute.account'),
    TextDyField.data_source('Instance ID', 'data.serverInstance.serverInstanceNo'),
    TextDyField.data_source('Instance Name', 'data.serverInstance.serverInstanceName'),
    EnumDyField.data_source('Instance State', 'data.compute.serverInstanceStatus', default_state={
        'safe': ['RUN'],
        'warning': ['NSTOP', 'FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'],
        'disable': [],
        'alert': ['SUSPENDED', 'TERMT']
    }),
    TextDyField.data_source('Instance Type', 'data.compute.serverInstancetype'),
    EnumDyField.data_source('Has GPU', 'data.display.has_gpu', default_badge={
        'indigo.500': ['True'], 'coral.600': ['False']}),
    TextDyField.data_source('Total GPU Count', 'data.Hardware.gpu_count'),
    ListDyField.data_source('GPUs', 'data.Hardware.gpu_machine_type',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
    TextDyField.data_source('Image', 'data.compute.serverImageName'),
    TextDyField.data_source('Region', 'data.Compute.region'),
    TextDyField.data_source('Self link', 'data.NPC.self_link'),
    TextDyField.data_source('Public IP', 'data.NIC.public_ip_address'),
    ListDyField.data_source('IP Addresses', 'NIC.ip_addresses',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
])

storage = TableDynamicLayout.set_fields('Storage', fields=[
    TextDyField.data_source('Name', 'data.Storage.storageName'),
    SizeField.data_source('Size', 'data.Storage.StorageSize'),
    EnumDyField.data_source('Disk Type', 'data.Storage.storageDiskType',
                            default_outline_badge=['local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard']),
])

server_engine = ListDynamicLayout.set_layouts('server engine',
                                              layouts=[server_instance])

server_instance_meta = CloudServiceMeta.set_layouts([server_engine, storage])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeServer')


class ServerInstanceResource(ComputeResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(ServerInstance)
    _metadata = ModelType(CloudServiceMeta, default=server_instance_meta, serialized_name='metadata')


class ServerInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ServerInstanceResource)
