from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.storage.object_storage.data import BucketGroup
# from spaceone.inventory.model.storage.object_storage.data import ArchiveBucketGroup
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
    TextDyField.data_source('Object Total Counts', 'data.object_count'),
    SizeField.data_source('Object Size', 'data.object_total_size'),
    DateTimeDyField.data_source('Created', 'data.creation_timestamp')

])

# bucket = ListDynamicLayout.set_layouts('bucket',
#                                             layouts=[bucket_instance])

bucket_instance_meta = CloudServiceMeta.set_layouts([bucket_instance])



class StorageGroupResource(CloudServiceResource):
    cloud_service_group = StringType(default='Storage')


class ObjectStorageResource(StorageGroupResource):
    cloud_service_type = StringType(default='ObjectStorage')
    data = ModelType(BucketGroup)
    _metadata = ModelType(CloudServiceMeta, default=bucket_instance_meta, serialized_name='metadata')

class ObjectStorageResponse(CloudServiceResponse):
    resource = PolyModelType(ObjectStorageResource)

