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
    EnumDyField.data_source('Instance State', 'state', default_state={
        'safe': ['ACTIVE']
    }),
    TextDyField.data_source('Desired Capacity', 'data.desired_capacity'),
    TextDyField.data_source('Minimum Size', 'data.min_size'),
    TextDyField.data_source('Maximum Size', 'data.max_size'),
    TextDyField.data_source('Health Check Type', 'data.health_check_type', options={'is_optional': True}),
    TextDyField.data_source('Health Check Grace Period', 'data.health_check_grace_period',
                            options={'is_optional': True}),
    TextDyField.data_source('Default Cooldown', 'data.default_cooldown', options={'is_optional': True})
])


autoscaling_instance_meta = CloudServiceMeta.set_layouts([autoscaling_instance])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compute')


class AutoscalingResource(ComputeResource):
    cloud_service_type = StringType(default='Autoscaling')
    data = ModelType(AutoScalingGroup)
    _metadata = ModelType(CloudServiceMeta, default=autoscaling_instance_meta, serialized_name='metadata')


class AutoscalingResponse(CloudServiceResponse):
    resource = PolyModelType(AutoscalingResource)
