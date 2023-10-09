from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.database.clouddb.data import Product
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

])

database = ListDynamicLayout.set_layouts('database',
                                            layouts=[cloud_db_instance])

cloud_db_instance_meta = CloudServiceMeta.set_layouts([database])


class ProductResource(CloudServiceResource):
    cloud_service_group = StringType(default='Database')


class CloudDBResource(ProductResource):
    cloud_service_type = StringType(default='CloudDB')
    data = ModelType(Product)
    _metadata = ModelType(CloudServiceMeta, default=cloud_db_instance_meta, serialized_name='metadata')


class CloudDBResponse(CloudServiceResponse):
    resource = PolyModelType(CloudDBResource)