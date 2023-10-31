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
count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yml')

cst_bucket = CloudServiceTypeResource()
cst_bucket.name = 'ArchiveStorage'
cst_bucket.provider = 'naver_cloud'
cst_bucket.group = 'CloudStorage'
cst_bucket.service_code = 'CloudStorage'
cst_bucket.labels = ['Storage']
cst_bucket.is_primary = True
cst_bucket.is_major = True
cst_bucket.tags = {
    'spaceone:icon': f'{ASSET_URL}/Cloud_Storage.svg',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Public Access', 'data.public_access', default_state={
            'safe': ['Subject to object ACLs', 'Not public'],
            'warning': ['Not authorized'],
            'alert': ['Public to internet'],
        }),


        TextDyField.data_source('Object Total Counts', 'data.object_count'),
        SizeField.data_source('Object Size', 'data.object_total_size'),
        TextDyField.data_source('Access Control', 'data.access_control'),
        TextDyField.data_source('Lifecycle rules', 'data.lifecycle_rule.lifecycle_rule_display'),
        EnumDyField.data_source('Requester Pays', 'data.requester_pays', default_badge={
            'indigo.500': ['OFF'], 'coral.600': ['ON']
        }),

    ],

    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Location', key='data.location.location'),
        SearchField.set(name='Object Counts', key='data.object_count', data_type='integer'),
        SearchField.set(name='Object Total Size (Bytes)', key='data.object_total_size', data_type='integer'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
        SearchField.set(name='Update Time', key='data.update_timestamp', data_type='datetime'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]