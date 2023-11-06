import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, ListDyField, SearchField, \
    EnumDyField, SizeField, DateTimeDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

#total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yml')
total_by_used_storage_conf = os.path.join(current_dir, 'widget/total_used_storage_size.yml')
total_by_storage_conf = os.path.join(current_dir, 'widget/total_storage_size.yml')

cst_database_cloud_db = CloudServiceTypeResource()
cst_database_cloud_db.name = 'CloudDB'
cst_database_cloud_db.provider = 'naver_cloud'
cst_database_cloud_db.group = 'Database'
cst_database_cloud_db.service_code = 'Cloud DB'
cst_database_cloud_db.labels = ['Database']
cst_database_cloud_db.is_primary = True
cst_database_cloud_db.is_major = True
cst_database_cloud_db.tags = {
    'spaceone:icon': f'{ASSET_URL}/Cloud_SQL.svg',
}

cst_database_cloud_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('State', 'data.cloud_db_instance_status_name', default_state={
            'safe': ['running'],
            'disable': ['deleting', 'creating', 'pending', 'recovering', 'restarting','reinstalling'],
            'alert': ['deleted'],
        }),
        TextDyField.data_source('DB Role', 'data.cloud_db_server_instance_list.cloud_db_server_role'),
        TextDyField.data_source('DB Engine Version', 'data.engine_version'),
        TextDyField.data_source('DB Server Name', 'data.cloud_db_server_instance_list.cloud_db_server_name'),
        SizeField.data_source('Used Storage Size', 'data.cloud_db_server_instance_list.used_data_storage', options={'is_optional': True}),
        SizeField.data_source('Data Storage Size', 'data.cloud_db_server_instance_list.data_storage_size'),
        TextDyField.data_source('Zone', 'data.zone_list.zone_name'),
        DateTimeDyField.data_source('Launched', 'launched_at', options={'is_optional': True}),
        TextDyField.data_source('Data Storage Type', 'data.data_storage_type', options={'is_optional': True}),
        TextDyField.data_source('Backup File Retention Period', 'data.backup_file_retention_period', options={'is_optional': True}),
        TextDyField.data_source('Backup Time', 'data.backup_time', options={'is_optional': True}),
        TextDyField.data_source('DB License', 'data.license_code', options={'is_optional': True}),
        TextDyField.data_source('uptime', 'data.cloud_db_server_instance_list.uptime', options={'is_optional': True}),
        TextDyField.data_source('DB Port', 'data.cloud_db_port', options={'is_optional': True}),
        TextDyField.data_source('DB Type', 'data.db_kind_code', options={'is_optional': True}),
        TextDyField.data_source('Private DNS Name', 'data.private_dns_name', options={'is_optional': True}),
        TextDyField.data_source('Public DNS Name', 'data.public_dns_name', options={'is_optional': True}),
    ],
    search=[
        SearchField.set(name='DB Service Name', key='name'),
        SearchField.set(name='DB Role', key='data.cloud_db_server_instance_list.cloud_db_server_role'),
        SearchField.set(name='DB Server Name', key='data.cloud_db_server_instance_list.cloud_db_server_name'),
        SearchField.set(name='DB Engine Version', key='data.engine_version'),
        SearchField.set(name='Used Data Storage(GB)', key='data.cloud_db_server_instance_list.used_data_storage'),
        SearchField.set(name='Data Storage(GB)', key='data.cloud_db_server_instance_list.data_storage_size'),
        SearchField.set(name='State', key='data.cloud_db_instance_status_name',
                        enums={
                                'RUN': {'label': 'Running'},
                                'NSTOP': {'label': 'Stopped'},
                                'ST_FL': {'label': 'Start Failed'},
                                'TERMT': {'label': 'Terminated'}
                            }),
        SearchField.set(name='Zone', key='data.zone_list.zone_name'),
        SearchField.set(name='Launched', key='launched_at'),
        SearchField.set(name='Region', key='data.region_code'),
        SearchField.set(name='DB License', key='data.license_code'),
        SearchField.set(name='CPU Count', key='data.cpu_count', data_type='integer'),
        SearchField.set(name='Data Storage Type', key='data.data_storage_type'),
        SearchField.set(name='DB Type', key='data.db_kind_code'),
        SearchField.set(name='Backup File Retention Period', key='data.backup_file_retention_period'),
        SearchField.set(name='Backup Time', key='data.backup_time'),
        SearchField.set(name='DB Port', key='data.cloud_db_port'),
        SearchField.set(name='uptime', key='data.cloud_db_server_instance_list.uptime'),
        SearchField.set(name='Private DNS Name', key='data.private_dns_name'),
        SearchField.set(name='Public DNS Name', key='data.public_dns_name'),

    ],

    widget=[
        #CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf)),
        ChartWidget.set(**get_data_from_yaml(total_by_used_storage_conf)),
        ChartWidget.set(**get_data_from_yaml(total_by_storage_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_database_cloud_db}),
]