from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.networking.vpc_network.data import *
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


'''
vpc Network
'''

VPC_instance = ItemDynamicLayout.set_fields('VPC Instance', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('DB Service Name', 'data.name'),
    ])
network_acl_list = ItemDynamicLayout.set_fields('Network ACL', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('DB Service Name', 'data.name'),
    ])
route_table_list = ItemDynamicLayout.set_fields('Route Table', fields=[
    ])
subnet_list = ItemDynamicLayout.set_fields('Subnet', fields=[
    ])

# TAB - Bucket
instance_template_meta = CloudServiceMeta.set_layouts([VPC_instance,
                                                       network_acl_list,
                                                       route_table_list,
                                                       subnet_list])


class VPCResource(CloudServiceResource):
    cloud_service_group = StringType(default='VPC')


class VPCNetworkResource(VPCResource):
    cloud_service_type = StringType(default='VPCNetwork')
    data = ModelType(VPC)
    _metadata = ModelType(CloudServiceMeta, default=instance_template_meta, serialized_name='metadata')


class VPCNetworkResponse(CloudServiceResponse):
    resource = PolyModelType(VPCNetworkResource)
