import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, ListDyField, SearchField, \
    EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yml')

cst_content_delivery_cdn = CloudServiceTypeResource()
cst_content_delivery_cdn.name = 'CDN'
cst_content_delivery_cdn.provider = 'naver_cloud'
cst_content_delivery_cdn.group = 'Content Delivery'
cst_content_delivery_cdn.service_code = 'CDN'
cst_content_delivery_cdn.labels = ['Content Delivery']
cst_content_delivery_cdn.is_primary = True
cst_content_delivery_cdn.is_major = True
cst_content_delivery_cdn.tags = {
    'spaceone:icon': f'{ASSET_URL}/Cloud_SQL.svg',
}

cst_content_delivery_cdn._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Nme', 'data.name'),
        TextDyField.data_source('Origin URL', 'data.cdn_plus_rule.origin_url'),
        EnumDyField.data_source('State', 'data.cdn_instance_status_name', default_state={
            'safe': ['RUNNING'],
            'disable': ['UNKNOWN', 'ON-DEMAND'],
            'alert': ['STOPPED'],
        }),
        TextDyField.data_source('Service Domain', 'data.cdn_plus_service_domain_list.default_domain_name'),
        DateTimeDyField.data_source('Launched', 'launched_at'),
        DateTimeDyField.data_source('Last Modified', 'data.last_modified_date',options={'is_optional': True}),
        TextDyField.data_source('Forward Host Header', 'data.cdn_plus_rule.forward_host_header_type_code', options={'is_optional': True}),
        TextDyField.data_source('Gzip Compression', 'data.cdn_plus_rule.is_gzip_compression_use', options={'is_optional': True}),
        TextDyField.data_source('Caching Option', 'data.cdn_plus_rule.caching_option_type_code', options={'is_optional': True}),
        TextDyField.data_source('Ignore Query String', 'data.cdn_plus_rule.is_query_string_ignore_use', options={'is_optional': True}),
        TextDyField.data_source('Referrer Domain', 'data.cdn_plus_rule.is_referrer_domain_use', options={'is_optional': True}),
        TextDyField.data_source('Large File Optimization', 'data.cdn_plus_rule.is_large_file_optimization_use', options={'is_optional': True}),
        TextDyField.data_source('Security Token', 'data.cdn_plus_rule.is_reissue_secure_token_password', options={'is_optional': True}),


    ],
    search=[
        SearchField.set(name='Service Domain', key='data.cdn_plus_service_domain_list.default_domain_name'),
        SearchField.set(name='Launched', key='launched_at'),
        SearchField.set(name='Last Modified', key='data.last_modified_date'),
        SearchField.set(name='Forward Host Header', key='data.cdn_plus_rule.forward_host_header_type_code'),
        SearchField.set(name='Gzip Compression', key='data.cdn_plus_rule.is_gzip_compression_use'),
        SearchField.set(name='Caching Option', key='data.cdn_plus_rule.caching_option_type_code'),
        SearchField.set(name='gnore Query String', key='data.cdn_plus_rule.is_query_string_ignore_use'),
        SearchField.set(name='Referrer Domain', key='data.cdn_plus_rule.is_referrer_domain_use'),
        SearchField.set(name='Large File Optimization', key='data.cdn_plus_rule.is_large_file_optimization_use'),
        SearchField.set(name='Security Token', key='data.cdn_plus_rule.is_reissue_secure_token_password'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_content_delivery_cdn}),
]