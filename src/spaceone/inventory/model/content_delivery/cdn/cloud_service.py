from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.content_delivery.cdn.data import CdnPlusInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
CloudDB
'''
cloud_db_instance = ItemDynamicLayout.set_fields('Monitoring Instance', fields=[

])

database = ListDynamicLayout.set_layouts('management',
                                            layouts=[cloud_db_instance])

cloud_db_instance_meta = CloudServiceMeta.set_layouts([database])


class InstancetResource(CloudServiceResource):
    cloud_service_group = StringType(default='content_delivery')


class CdnResource(InstancetResource):
    cloud_service_type = StringType(default='cdn')
    data = ModelType(CdnPlusInstance)
    _metadata = ModelType(CloudServiceMeta, default=cloud_db_instance_meta, serialized_name='metadata')


class CdnResponse(CloudServiceResponse):
    resource = PolyModelType(CdnResource)