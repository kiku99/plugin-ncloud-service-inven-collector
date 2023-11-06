import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')

cst_bucket= CloudServiceTypeResource()
cst_bucket.name = 'ObjectStorage'
cst_bucket.provider = 'naver_cloud'
cst_bucket.group = 'Storage'
cst_bucket.service_code = 'ObjectStorage'
cst_bucket.labels = ['Storage', 'ObjectStorage']
cst_bucket.is_primary = True
cst_bucket.is_major = True
cst_bucket.tags = {
    'spaceone:icon': f'{ASSET_URL}/Cloud_Storage.svg',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.buckets.name'),
        DateTimeDyField.data_source('Creation Date', 'data.buckets.creation_date'),
        TextDyField.data_source('Display Name', 'data.owner.display_name'),
        TextDyField.data_source('ID', 'data.owner.id')
    ],

    search=[
        SearchField.set(name='ID', key='data.owner.id'),
        SearchField.set(name='Name', key='data.buckets.name'),
        SearchField.set(name='Cration Date', key='data.buckets.creation_date'),
        SearchField.set(name='Display Name', key='data.owner.display_name')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]