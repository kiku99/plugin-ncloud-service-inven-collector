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

])

bucket = ListDynamicLayout.set_layouts('bucket',
                                            layouts=[bucket_instance])

bucket_instance_meta = CloudServiceMeta.set_layouts([bucket])



class StorageGroupResource(CloudServiceResource):
    cloud_service_group = StringType(default='CloudStorage')


class ObjectStorageResource(StorageGroupResource):
    cloud_service_type = StringType(default='ObjectStorage')
    data = ModelType(BucketGroup)
    _metadata = ModelType(CloudServiceMeta, default=bucket_instance_meta, serialized_name='metadata')

class ObjectStorageResponse(CloudServiceResponse):
    resource = PolyModelType(ObjectStorageResource)

# class ArchiveStorageResource(StorageGroupResource):
#     cloud_service_type = StringType(default='Bucket')
#     data = ModelType(ArchiveBucketGroup)
#     _metadata = ModelType(CloudServiceMeta, default=bucket_instance_meta, serialized_name='metadata')
#
# class ArchiveStorageResponse(CloudServiceResponse):
#     resource = PolyModelType(ArchiveStorageResource)