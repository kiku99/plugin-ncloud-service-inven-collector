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

cst_bucket = CloudServiceTypeResource()
cst_bucket.name = 'ArchiveStorage'
cst_bucket.provider = 'naver_cloud'
cst_bucket.group = 'Storage'
cst_bucket.service_code = 'ArchiveStorage'
cst_bucket.labels = ['Storage', 'ArchiveStorage']
cst_bucket.is_primary = True
cst_bucket.is_major = True
cst_bucket.tags = {
    'spaceone:icon': f'{ASSET_URL}/Cloud_Storage.svg',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        SizeField.data_source('Count', 'data.count'),
        SizeField.data_source('Size', 'data.bytes'),
        DateTimeDyField.data_source('Last Modified', 'data.last_modified'),
        DateTimeDyField.data_source('Launched', 'launched_at')

    ],

    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Archive Counts', key='data.count', data_type='integer'),
        SearchField.set(name='Archive Total Size (Bytes)', key='data.bytes', data_type='integer'),
        SearchField.set(name='Last Modified', key='data.last_modified', data_type='datetime'),
        SearchField.set(name='Launched', key='launched_at', data_type='datetime'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]