from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.storage.data import BucketGroup
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
Bucket
'''
# TAB - Bucket
bucket_instance = ItemDynamicLayout.set_fields('Bucket Instance', fields=[

])

bucket = ListDynamicLayout.set_layouts('bucket',
                                            layouts=[bucket_instance])

bucket_instance_meta = CloudServiceMeta.set_layouts([bucket])



class StorageGroupResource(CloudServiceResource):
    cloud_service_group = StringType(default='bucket')


class ObjectStorageResource(StorageGroupResource):
    cloud_service_type = StringType(default='Bucket')
    data = ModelType(BucketGroup) #여기 괄호 수정함
    _metadata = ModelType(CloudServiceMeta, default=bucket_instance_meta, serialized_name='metadata')


class ObjectStorageResponse(CloudServiceResponse):
    resource = PolyModelType(ObjectStorageResource)