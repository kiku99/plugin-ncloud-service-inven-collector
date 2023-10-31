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
total_disk_size_conf = os.path.join(current_dir, 'widget/total_disk_size.yml')
total_memory_size_conf = os.path.join(current_dir, 'widget/total_memory_size.yml')
total_vcpu_count_conf = os.path.join(current_dir, 'widget/total_vcpu_count.yml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yml')
count_by_instance_type_conf = os.path.join(current_dir, 'widget/count_by_instance_type.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')

cst_server_instance = CloudServiceTypeResource()
cst_server_instance.name = 'Instance'
cst_server_instance.provider = 'naver_cloud'
cst_server_instance.group = 'Compute'
cst_server_instance.service_code = 'Server'
cst_server_instance.labels = ['Compute', 'Server']
cst_server_instance.is_primary = True
cst_server_instance.is_major = True
cst_server_instance.tags = {'spaceone:icon': f'{ASSET_URL}/Compute_Engine.svg', }

cst_server_instance._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Instance State', 'data.compute.instance_state', default_state={
            'safe': ['RUNNING'],
            'warning': ['STAGING', 'PROVISIONING', 'REPAIRING', 'STOPPING', 'SUSPENDING'],
            'disable': [],
            'alert': ['SUSPENDED', 'TERMINATED']
        }),
        TextDyField.data_source('Server ID', 'server_id', options={'is_optional': True}),
        TextDyField.data_source('Instance Type', 'data.compute.instance_type'),
        TextDyField.data_source('Core', 'data.hardware.core'),
        TextDyField.data_source('Memory', 'data.hardware.memory'),
        TextDyField.data_source('Preemptible', 'data.compute.scheduling.preemptible', options={'is_optional': True}),
        TextDyField.data_source('Instance ID', 'data.compute.instance_id', options={'is_optional': True}),
        TextDyField.data_source('Image', 'data.compute.image', options={'is_optional': True}),
        TextDyField.data_source('Availability Zone', 'data.compute.az'),
        TextDyField.data_source('Primary IP', 'data.primary_ip_address', options={'is_optional': True}),
        TextDyField.data_source('Public IP', 'data.compute.public_ip_address', options={'is_optional': True}),
        TextDyField.data_source('Account ID', 'account', options={'is_optional': True}),
        TextDyField.data_source('Launched', 'launched_at', options={'is_optional': True}),
    ],

    search=[
        SearchField.set(name='Server ID', key='server_id'),
        SearchField.set(name='IP Address', key='data.ip_addresses'),
        SearchField.set(name='Instance ID', key='data.compute.instance_id'),
        SearchField.set(name='Instance State', key='data.compute.instance_state',
                        enums={
                            'RUNNING': {'label': 'Running'},
                            'STOPPED': {'label': 'Stopped'},
                            'DEALLOCATED': {'label': 'Deallocated'},
                            'SUSPENDED': {'label': 'Suspended'},
                            'TERMINATED': {'label': 'Terminated'}
                        }),
        SearchField.set(name='Instance Type', key='data.compute.instance_type'),
        SearchField.set(name='Key Pair', key='data.compute.keypair'),
        SearchField.set(name='Availability Zone', key='data.compute.az'),
        SearchField.set(name='Public IP Address', key='data.nics.public_ip_address'),
        SearchField.set(name='Public DNS', key='data.nics.tags.public_dns'),
        SearchField.set(name='Memory', key='data.hardware.memory', data_type='float'),
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
    CloudServiceTypeResponse({'resource': cst_server_instance}),
]
