import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
total_disk_size_conf = os.path.join(current_dir, 'widget/total_disk_size.yml')
total_memory_size_conf = os.path.join(current_dir, 'widget/total_memory_size.yml')
total_vcpu_count_conf = os.path.join(current_dir, 'widget/total_vcpu_count.yml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yml')
count_by_instance_type_conf = os.path.join(current_dir, 'widget/count_by_instance_type.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')

cst_server = CloudServiceTypeResource()
cst_server.name = 'Server'
cst_server.provider = 'naver_cloud'
cst_server.group = 'Compute'
cst_server.service_code = 'Server'
cst_server.labels = ['Compute', 'Server']
cst_server.is_primary = True
cst_server.is_major = True
cst_server.tags = {'spaceone:icon': f'{ASSET_URL}/Compute_Engine.svg', }

cst_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Instance State', 'data.compute.server_instance_status', default_state={
            'safe': ['RUN'],
            'warning': ['INIT', 'CREAT', 'NSTOP'],
            'disable': ['FSTOP', 'SD_FL', 'RS_FL', 'ST_FL'],
            'alert': ['TERMT']
        }),
        TextDyField.data_source('Server ID', 'server_id', options={'is_optional': True}),
        TextDyField.data_source('Instance Type', 'data.compute.server_instance_type'),
        TextDyField.data_source('Core', 'data.hardware.cpu_count'),
        SizeField.data_source('Memory', 'data.hardware.memory_size'),
        TextDyField.data_source('Image', 'data.compute.server_image_name', options={'is_optional': True}),
        TextDyField.data_source('Availability Zone', 'data.compute.zone'),
        TextDyField.data_source('Private IP', 'data.ip.private_ip', options={'is_optional': True}),
        TextDyField.data_source('Public IP', 'data.ip.public_ip', options={'is_optional': True}),
        TextDyField.data_source('Account ID', 'account', options={'is_optional': True}),
        TextDyField.data_source('Launched', 'launched_at', options={'is_optional': True}),
    ],

    search=[
        SearchField.set(name='Server ID', key='server_id'),
        SearchField.set(name='Instance State', key='data.compute.server_instance_status',
                        enums={
                            'RUN': {'label': 'Running'},
                            'NSTOP': {'label': 'Stopped'},
                            'ST_FL': {'label': 'Start Failed'},
                            'TERMT': {'label': 'Terminated'}
                        }),
        SearchField.set(name='Instance Type', key='data.compute.server_instance_type'),
        SearchField.set(name='Availability Zone', key='data.compute.zone'),
        SearchField.set(name='Memory', key='data.hardware.memory_size', data_type='float'),
        SearchField.set(name='Account ID', key='account'),
        SearchField.set(name='Launched', key='launched_at'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_vcpu_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_memory_size_conf)),
        CardWidget.set(**get_data_from_yaml(total_disk_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_instance_type_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_server}),
]
