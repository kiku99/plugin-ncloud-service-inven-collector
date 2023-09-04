from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.compute.server.data import ServerInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, \
    DateTimeDyField, SizeField, MoreField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
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
    # TextDyField.data_source('Availability Zone', 'data.compute.az'),
    # TextDyField.data_source('Reservation Affinity', 'data.NaverCloud.reservation_affinity'),
    TextDyField.data_source('Self link', 'data.NPC.self_link'),
    # EnumDyField.data_source('Deletion Protection', 'data.NaverCloud.deletion_protection', default_badge={
    #     'indigo.500': ['true'], 'coral.600': ['false']
    # }),
    TextDyField.data_source('Public IP', 'data.NIC.public_ip_address'),
    ListDyField.data_source('IP Addresses', 'NIC.ip_addresses',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
    # ListDyField.data_source('Affected Rules', 'data.compute.security_groups',
    #                         default_badge={'type': 'outline', 'delimiter': '<br>'}),
    #     DateTimeDyField.data_source('Launched At', 'data.compute.launched_at'),
])

naver_cloud_vpc = ItemDynamicLayout.set_fields('VPC', fields=[
    TextDyField.data_source('VPC ID', 'data.VPC.vpc_id'),
    TextDyField.data_source('VPC Name', 'data.VPC.vpc_name'),
    TextDyField.data_source('Subnet ID', 'data.Subnet.subnet_id'),
    TextDyField.data_source('Subnet Name', 'data.Subnet.subnet_name'),
])

# instance_group_manager = ItemDynamicLayout.set_fields('InstanceGroupManager', fields=[
#     TextDyField.data_source('Auto Scaler', 'data.Autoscaler.name'),
#     TextDyField.data_source('Auto Scaler ID', 'data.Autoscaler.id'),
#     TextDyField.data_source('Instance Group Name', 'data.Autoscaler.instance_group.name'),
#     TextDyField.data_source('Instance Template Name', 'data.Autoscaler.instance_group.instance_template_name'),
# ])

operating_system_manager = ItemDynamicLayout.set_fields('Operating System', fields=[
    TextDyField.data_source('OS Type', 'data.OS.os_type'),
    TextDyField.data_source('OS Distribution', 'data.OS.os_distro'),
    TextDyField.data_source('OS Architecture', 'data.OS.os_arch'),
    TextDyField.data_source('OS Version Details', 'data.OS.details'),
    # TextDyField.data_source('OS License', 'data.os.os_license'),
])

hardware_manager = ItemDynamicLayout.set_fields('Hardware', root_path='data.Hardware', fields=[
    # Te=xtDyField.data_source('Core', 'core'),
    TextDyField.data_source('Memory', 'memorySize'),
    TextDyField.data_source('CPU Model', 'cpu_machine_type'),
])

storage = TableDynamicLayout.set_fields('Storage', fields=[
    # TextDyField.data_source('Index', ''),  # 어디꺼를 가져오는거지?
    TextDyField.data_source('Name', 'data.Storage.storageName'),
    SizeField.data_source('Size', 'data.Storage.StorageSize'),
    # TextDyField.data_source('Disk ID', 'tags.disk_id'),
    EnumDyField.data_source('Disk Type', 'data.Storage.storageDiskType',
                            default_outline_badge=['local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard']),
    # TextDyField.data_source('Read IOPS', 'tags.read_iops'),
    # TextDyField.data_source('Write IOPS', 'tags.write_iops'),
    # TextDyField.data_source('Read Throughput(MB/s)', 'tags.read_throughput'),
    # TextDyField.data_source('Write Throughput(MB/s)', 'tags.write_throughput'),
    # EnumDyField.data_source('Encrypted', 'tags.encrypted', default_badge={
    #     'indigo.500': ['true'], 'coral.600': ['false']
    # }),
])

nic = TableDynamicLayout.set_fields('NIC', root_path='data.NIC', fields=[
    TextDyField.data_source('Index', 'device_index'),
    ListDyField.data_source('IP Addresses', 'ip_addresses', options={'delimiter': '<br>'}),
    TextDyField.data_source('CIDR', 'cidr'),
    TextDyField.data_source('Public IP', 'public_ip_address'),
    TextDyField.data_source('Device', 'device'),
    TextDyField.data_source('Mac Addresses', 'mac_address')
])

Tags = TableDynamicLayout.set_fields('Labels', root_path='data.InstanceTag', fields=[
    TextDyField.data_source('Key', 'tagkey'),
    TextDyField.data_source('Value', 'tagValue'),
])

server_engine = ListDynamicLayout.set_layouts('server engine',
                                              layouts=[server_instance, naver_cloud_vpc])

server_instance_meta = CloudServiceMeta.set_layouts([server_engine, Tags, storage, nic])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeServer')


class ServerInstanceResource(ComputeResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(ServerInstance)
    _metadata = ModelType(CloudServiceMeta, default=server_instance_meta, serialized_name='metadata')


class ServerInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ServerInstanceResource)
