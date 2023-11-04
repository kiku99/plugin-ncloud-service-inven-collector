import os

from spaceone.inventory.conf.cloud_service_conf import ASSET_URL
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')

cst_server_instance = CloudServiceTypeResource()
cst_server_instance.name = 'Autoscaling'
cst_server_instance.provider = 'naver_cloud'
cst_server_instance.group = 'Compute'
cst_server_instance.service_code = 'Autoscaling'
cst_server_instance.labels = ['Compute', 'Autoscaling']
cst_server_instance.is_primary = True
cst_server_instance.is_major = True
cst_server_instance.tags = {'spaceone:icon': f'{ASSET_URL}/Compute_Engine.svg', }

cst_server_instance._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Instance State', 'state', default_state={
            'safe': ['ACTIVE']
        }),
        TextDyField.data_source('Desired Capacity', 'data.desired_capacity'),
        TextDyField.data_source('Minimum Size', 'data.min_size'),
        TextDyField.data_source('Maximum Size', 'data.max_size'),
        TextDyField.data_source('Health Check Type', 'data.health_check_type', options={'is_optional': True}),
        TextDyField.data_source('Health Check Grace Period', 'data.health_check_grace_period', options={'is_optional': True}),
        TextDyField.data_source('Default Cooldown', 'data.default_cooldown', options={'is_optional': True})
    ],

    search=[
        SearchField.set(name='Instance State', key='state',
                        enums={
                            'ACTIVE': {'label': 'Active'}
                        }),
        SearchField.set(name='Desired Capacity', key='data.desired_capacity'),
        SearchField.set(name='Minimum Size', key='data.min_size'),
        SearchField.set(name='Maximum Size', key='data.max_size'),
        SearchField.set(name='Health Check Type', key='data.health_check_type'),
        SearchField.set(name='Health Check Grace Period', key='data.health_check_grace_period'),
        SearchField.set(name='Default Cooldown', key='data.default_cooldown')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_server_instance}),
]
