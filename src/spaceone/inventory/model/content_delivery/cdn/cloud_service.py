from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.content_delivery.cdn.data import CdnPlusInstance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceMeta, CloudServiceResource, \
    CloudServiceResponse

'''
CDN
'''
cdn_instance = ItemDynamicLayout.set_fields('CDN Instance',fields=[
    EnumDyField.data_source('State', 'data.cdn_instance_status_name', default_state={
        'safe': ['running'],
        'disable': ['deleting', 'creating', 'pending', 'recovering', 'restarting', 'reinstalling'],
        'alert': ['deleted']
    }),
    TextDyField.data_source('Instance Operation', 'data.cdn_instance_operation'),
    TextDyField.data_source('Partial Domain Purge', 'data.is_available_partial_domain_purge'),
    TextDyField.data_source('Live Transcoder', 'data.is_for_live_transcoder'),
    TextDyField.data_source('Image Optimizer', 'data.is_for_image_optimizer'),
    TextDyField.data_source('Last Modified Date', 'data.last_modified_date'),
    TextDyField.data_source('Instance Operation', 'data.cdn_instance_operation'),


])
cdn_plus_rule = ItemDynamicLayout.set_fields('CDN Rule',fields=[
    TextDyField.data_source('Cache Key Host Name', 'data.cdn_plus_rule.cache_key_host_name_type_code'),
    TextDyField.data_source('Cache Option', 'data.cdn_plus_rule.caching_option_type_code'),
    TextDyField.data_source('Forward Host Header', 'data.cdn_plus_rule.forward_host_header_type_code'),
    TextDyField.data_source('Gzip Compression', 'data.cdn_plus_rule.is_gzip_compression_use'),
    TextDyField.data_source('Large File Optimization', 'data.cdn_plus_rule.is_large_file_optimization_use'),
    TextDyField.data_source('Origin Http Port', 'data.cdn_plus_rule.origin_http_port'),
    TextDyField.data_source('Origin Https Port', 'data.cdn_plus_rule.origin_https_port'),
    TextDyField.data_source('Origin Url', 'data.cdn_plus_rule.origin_url'),
    TextDyField.data_source('Protocol', 'data.cdn_plus_rule.protocol_type_code'),
    TextDyField.data_source('Ignore Query String', 'data.cdn_plus_rule.is_query_string_ignore_use'),
    TextDyField.data_source('Referrer Domain', 'data.cdn_plus_rule.is_referrer_domain_use'),
    TextDyField.data_source('Referrer Domain Restrict', 'data.cdn_plus_rule.is_referrer_domain_restrict_use'),

])
cdn_plus_service_domain = ItemDynamicLayout.set_fields('CDN Service Domain', fields=[
    TextDyField.data_source('Default Domain Name', 'data.cdn_plus_service_domain_list.default_domain_name'),
    TextDyField.data_source('Domain Id', 'data.cdn_plus_service_domain_list.domain_id'),
    TextDyField.data_source('Protocol', 'data.cdn_plus_service_domain_list.protocol_type_code'),


])


cdn_instance_meta = CloudServiceMeta.set_layouts([cdn_instance, cdn_plus_rule, cdn_plus_service_domain])


class InstanceResource(CloudServiceResource):
    cloud_service_group = StringType(default='Content Delivery')


class CdnResource(InstanceResource):
    cloud_service_type = StringType(default='CDN')
    data = ModelType(CdnPlusInstance)
    _metadata = ModelType(CloudServiceMeta, default=cdn_instance_meta, serialized_name='metadata')


class CdnResponse(CloudServiceResponse):
    resource = PolyModelType(CdnResource)