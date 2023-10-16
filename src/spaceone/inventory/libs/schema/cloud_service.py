from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, FloatType, DateTimeType
from .base import BaseMetaData, BaseResponse, MetaDataView, MetaDataViewSubData


class CloudServiceMeta(BaseMetaData):
    @classmethod
    def set(cls):
        sub_data = MetaDataViewSubData()
        return cls({'view': MetaDataView({'sub_data': sub_data})})

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})


class CloudServiceResource(Model):
    provider = StringType(default="naver_cloud")
    account = StringType(default="")
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    name = StringType(default="")
    region_code = StringType(default="")
    data = PolyModelType(Model, default=lambda: {})
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    provider = StringType(default="naver_cloud")
    cloud_service_group = StringType(default='Compute', serialize_when_none=False)
    cloud_service_type = StringType(default='Server', serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)


class ErrorResourceResponse(CloudServiceResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    resource = ModelType(ErrorResource, default={})

class BaseResource(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    project = StringType(serialize_when_none=False)
    region = StringType(serialize_when_none=False)
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    #google_cloud_monitoring = ModelType(GoogleCloudMonitoringModel, serialize_when_none=False)
    #google_cloud_logging = ModelType(GoogleCloudLoggingModel, serialize_when_none=False)