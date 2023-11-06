from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.networking.vpc_network.data import *
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


'''
vpc Network
'''

VPC_instance = ItemDynamicLayout.set_fields('VPC Instance', fields=[
    TextDyField.data_source('CIDR Block', 'data.ipv4_cidr_block'),
    EnumDyField.data_source('State', 'data.vpc_status', default_state={
        'safe': ['RUN'],
        'warning': ['CREATING', 'INIT'],
        'alert': ['TERMTING']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_no'),
    TextDyField.data_source('Region', 'data.region_code'),

    ])
network_acl_list = ItemDynamicLayout.set_fields('Network ACL', fields=[
    TextDyField.data_source('Default', 'data.network_acl_list.is_default'),
    TextDyField.data_source('Network ACL ID', 'data.network_acl_list.network_acl_no'),
    TextDyField.data_source('Network ACL Name', 'data.network_acl_list.network_acl_name'),
    EnumDyField.data_source('State', 'data.network_acl_list.network_acl_status', default_state={
        'safe': ['RUN'],
        'warning': ['CREATING', 'INIT'],
        'alert': ['TERMTING']
    }),
    ListDyField.data_source('Description', 'data.network_acl_list.network_acl_description'),
    ])
route_table_list = ItemDynamicLayout.set_fields('Route Table', fields=[
    TextDyField.data_source('Default', 'data.route_table_list.is_default'),
    TextDyField.data_source('Route Table ID', 'data.route_table_list.route_table_no'),
    TextDyField.data_source('Route Table Name', 'data.route_table_list.route_table_name'),
    EnumDyField.data_source('State', 'data.route_table_list.route_table_status', default_state={
        'safe': ['RUN'],
        'warning': ['CREATING', 'INIT'],
        'alert': ['TERMTING']
    }),
    ListDyField.data_source('Description', 'data.route_table_list.route_table_description'),
    TextDyField.data_source('Subnet Type', 'data.route_table_list.subnet_type'),

    ])
subnet_list = ItemDynamicLayout.set_fields('Subnet', fields=[
    TextDyField.data_source('Subnet ID', 'data.subnet_list.subnet_no'),
    TextDyField.data_source('Subnet Name', 'data.subnet_list.subnet_name'),
    EnumDyField.data_source('State', 'data.subnet_list.subnet_status', default_state={
        'safe': ['RUN'],
        'warning': ['CREATING', 'INIT'],
        'alert': ['TERMTING']
    }),
    TextDyField.data_source('Availability Zone', 'data.subnet_list.zone_code'),
    TextDyField.data_source('VPC ID', 'data.subnet_list.vpc_no'),
    TextDyField.data_source('Network ACL ID', 'data.subnet_list.network_acl_no'),
    ListDyField.data_source('Description', 'data.subnet_list.subnet_description'),
    TextDyField.data_source('Subnet Type', 'data.subnet_list.subnet_type'),
    TextDyField.data_source('Usage Type', 'data.subnet_list.subnet_usage_type'),



    ])

# TAB - Bucket
instance_template_meta = CloudServiceMeta.set_layouts([VPC_instance,
                                                       network_acl_list,
                                                       route_table_list,
                                                       subnet_list])


class VPCResource(CloudServiceResource):
    cloud_service_group = StringType(default='Networking')


class VPCNetworkResource(VPCResource):
    cloud_service_type = StringType(default='VPCNetwork')
    data = ModelType(VPC)
    _metadata = ModelType(CloudServiceMeta, default=instance_template_meta, serialized_name='metadata')


class VPCNetworkResponse(CloudServiceResponse):
    resource = PolyModelType(VPCNetworkResource)
