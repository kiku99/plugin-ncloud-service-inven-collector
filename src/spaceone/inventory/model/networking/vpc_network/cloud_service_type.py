import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yml')

cst_network = CloudServiceTypeResource()
cst_network.name = 'VPCNetwork'
cst_network.provider = 'naver_cloud'
cst_network.group = 'Networking'
cst_network.service_code = 'VPC'
cst_network.is_primary = True
cst_network.labels = ['Networking']
cst_network.tags = {
    'spaceone:icon': f'{ASSET_URL}/vpc.svg',}

cst_network._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('VPC Name', 'name'),
        TextDyField.data_source('VPC ID', 'data.vpc_no'),
        TextDyField.data_source('CIDR Block', 'data.ipv4_cidr_block'),
        EnumDyField.data_source('State', 'data.vpc_status', default_state={
            'safe': ['RUN'],
            'warning': ['CREATING', 'INIT'],
            'alert': ['TERMTING']
        }),
        DateTimeDyField.data_source('Launched', 'launched_at', options={
            'is_optional': True
        }),
        TextDyField.data_source('Region', 'data.region_code', options={
            'is_optional': True
        }),

    ],

    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='description', key='data.description'),
        SearchField.set(name='firewall', key='data.firewall_data.firewall'),
        SearchField.set(name='route', key='data.route_data.route'),
        SearchField.set(name='subnetwork', key='data.subnetwork_data.subnets'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_network}),
]
