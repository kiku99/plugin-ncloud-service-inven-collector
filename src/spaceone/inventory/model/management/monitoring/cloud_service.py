from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.management.monitoring.data import Metric, MetricStatistic
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


class MetricstResource(CloudServiceResource):
    cloud_service_group = StringType(default='Management')


class MonitoringResource(MetricstResource):
    cloud_service_type = StringType(default='Monitoring')
    data = ModelType(Metric)
    _metadata = ModelType(CloudServiceMeta, default=cloud_db_instance_meta, serialized_name='metadata')


class MonitoringResponse(CloudServiceResponse):
    resource = PolyModelType(MonitoringResource)