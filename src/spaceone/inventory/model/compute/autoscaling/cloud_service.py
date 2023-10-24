from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.compute.autoscaling.data import AutoScalingGroup
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
Autoscaling
'''
autoscaling_instance = ItemDynamicLayout.set_fields('Autoscaling Instance', fields=[

])

server_engine = ListDynamicLayout.set_layouts('server engine',
                                              layouts=[autoscaling_instance])

autoscaling_instance_meta = CloudServiceMeta.set_layouts([server_engine])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class AutoscalingResource(ComputeResource):
    cloud_service_type = StringType(default='Autoscaling')
    data = ModelType(AutoScalingGroup)
    _metadata = ModelType(CloudServiceMeta, default=autoscaling_instance_meta, serialized_name='metadata')


class AutoscalingResponse(CloudServiceResponse):
    resource = PolyModelType(AutoscalingResource)
