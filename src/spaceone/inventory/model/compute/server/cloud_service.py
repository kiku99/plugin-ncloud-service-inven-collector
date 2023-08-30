from schematics.types import ModelType, StringType, PolyModelType

from src.spaceone.inventory.model.compute.server.data import ServerInstance
from src.spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, \
    DateTimeDyField, SizeField, MoreField
from src.spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from src.spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
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
#
# service_accounts = TableDynamicLayout.set_fields('API and Identity Management',
#                                                  root_path='data.NaverCloud.service_accounts', fields=[
#         TextDyField.data_source('Service Account', 'service_account'),
#         MoreField.data_source('Cloud API access scopes', 'display_name',
#                               options={
#                                   'layout': {
#                                       'name': 'Details',
#                                       'options': {
#                                           'type': 'popup',
#                                           'layout': {
#                                               'type': 'simple-table',
#                                               'options': {
#                                                   'root_path': 'scopes',
#                                                   'fields': [
#                                                       {
#                                                           "type": "text",
#                                                           "key": "description",
#                                                           "name": "Scope Description"
#                                                       }
#                                                   ]
#                                               }
#                                           }
#                                       }
#                                   }
#                               })
#     ])



storage = TableDynamicLayout.set_fields('Storage', root_path='data.Storage', fields=[
    TextDyField.data_source('Index', 'device_index'),  # 어디꺼를 가져오는거지?
    TextDyField.data_source('Name', 'tags.disk_name'),
    SizeField.data_source('Size', 'size'),
    TextDyField.data_source('Disk ID', 'tags.disk_id'),
    EnumDyField.data_source('Disk Type', 'tags.disk_type',
                            default_outline_badge=['local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard']),
    TextDyField.data_source('Read IOPS', 'tags.read_iops'),
    TextDyField.data_source('Write IOPS', 'tags.write_iops'),
    TextDyField.data_source('Read Throughput(MB/s)', 'tags.read_throughput'),
    TextDyField.data_source('Write Throughput(MB/s)', 'tags.write_throughput'),
    EnumDyField.data_source('Encrypted', 'tags.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

nic = TableDynamicLayout.set_fields('NIC', root_path='data.NIC', fields=[
    TextDyField.data_source('Index', 'device_index'),
    ListDyField.data_source('IP Addresses', 'ip_addresses', options={'delimiter': '<br>'}),
    TextDyField.data_source('CIDR', 'cidr'),
    TextDyField.data_source('Public IP', 'public_ip_address')
])

firewall = TableDynamicLayout.set_fields('Firewalls', root_path='data.securityGroup', fields=[
    TextDyField.data_source('Priority', 'priority'),
    EnumDyField.data_source('Direction', 'direction', default_badge={
        'indigo.500': ['ingress'], 'coral.600': ['egress']
    }),
    EnumDyField.data_source('Action', 'action', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
    TextDyField.data_source('Name', 'security_group_name'),
    TextDyField.data_source('Firewall ID', 'security_group_id'),
    TextDyField.data_source('Protocol', 'protocol'),
    TextDyField.data_source('Port Min.', 'port_range_min'),
    TextDyField.data_source('Port MAx.', 'port_range_max'),
    TextDyField.data_source('Description', 'description'),
])

lb = TableDynamicLayout.set_fields('LB', root_path='data.loadBalancer', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Type', 'type', default_badge={
        'primary': ['HTTP', 'HTTPS'], 'indigo.500': ['TCP'], 'coral.600': ['UDP']
    }),
    ListDyField.data_source('Protocol', 'protocol', options={'delimiter': '<br>'}),
    ListDyField.data_source('Port', 'port', options={'delimiter': '<br>'}),
    EnumDyField.data_source('Scheme', 'scheme', default_badge={
        'indigo.500': ['EXTERNAL'], 'coral.600': ['INTERNAL']
    }),
])

labels = TableDynamicLayout.set_fields('Labels', root_path='data.NaverCloud.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

tags = TableDynamicLayout.set_fields('Tags', root_path='data.NaverCloud.tags', fields=[
    TextDyField.data_source('Item', 'key')
])

server_engine = ListDynamicLayout.set_layouts('server engine',
                                              layouts=[server_instance, naver_cloud_vpc])

server_instance_meta = CloudServiceMeta.set_layouts([server_engine, labels, tags, storage, nic, firewall, lb])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class ServerInstanceResource(ComputeResource):
    cloud_service_type = StringType(default='Server')
    data = ModelType(ServerInstance)
    _metadata = ModelType(CloudServiceMeta, default=server_instance_meta, serialized_name='metadata')


class ServerInstanceResponse(CloudServiceResponse):
    resource = PolyModelType(ServerInstanceResource)


