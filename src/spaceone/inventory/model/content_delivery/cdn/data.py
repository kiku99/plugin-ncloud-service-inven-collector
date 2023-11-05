from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class CdnPlusServiceDomain(Model):
    domain_id = StringType()
    service_domain_type_code = StringType()
    protocol_type_code = StringType()
    default_domain_name = StringType()
    user_domain_name = StringType()

class CdnPlusPurgeHistory(Model):
    cdn_instance_no = StringType()
    purge_id = StringType()
    is_whole_purge = BooleanType()
    is_whole_domain = BooleanType()
    cdn_plus_service_domain_list = ListType(ModelType(CdnPlusServiceDomain))
    target_directory_name = StringType()
    target_file_list = ListType(StringType)
    request_date = StringType()
    purge_status_name = StringType()

class CdnPlusRule(Model):
    protocol_type_code = StringType()
    service_domain_type_code = StringType()
    origin_url = StringType()
    origin_http_port = IntType()
    origin_https_port = IntType()
    forward_host_header_type_code = StringType()
    cache_key_host_name_type_code = StringType()
    caching_option_type_code = StringType()
    caching_ttl_time = IntType()
    gzip_response_type_code = StringType()
    is_access_log_use = BooleanType()
    is_error_contents_response_use = BooleanType()
    is_gzip_compression_use = BooleanType()
    is_large_file_optimization_use = BooleanType()
    is_query_string_ignore_use = BooleanType()
    is_referrer_domain_restrict_use = BooleanType()
    is_referrer_domain_use = BooleanType()
    is_reissue_secure_token_password = BooleanType()




class CdnPlusInstance(Model):
    #cdn_instance_no = StringType()
    cdn_instance_status = StringType()
    cdn_instance_operation = StringType()
    cdn_instance_status_name = StringType()
    #create_date = StringType()
    last_modified_date = StringType()
    #cdn_instance_description = StringType()
    service_name = StringType()
    is_for_live_transcoder = BooleanType()
    #live_transcoder_instance_no_list = ListType(StringType)
    is_for_image_optimizer = BooleanType()
    #image_optimizer_instance_no = StringType()
    is_available_partial_domain_purge = BooleanType()
    cdn_plus_service_domain_list =ListType(ModelType(CdnPlusServiceDomain))
    cdn_plus_rule = ListType(ModelType(CdnPlusRule))


class GlobalCdnServiceDomain(Model):
    service_domain_type_code = StringType()
    protocol_type_code = StringType()
    default_domain_name = StringType()
    user_domain_name = StringType()

class GlobalCdnRule(Model):
    protocol_type_code = StringType()
    service_domain_type_code = StringType()
    origin_url = StringType()
    originHttpPort = StringType()
    originHttpsPort = StringType()
    forward_host_header_type_code = StringType()
    cache_key_host_name_type_code = StringType()
    caching_option_type_code = StringType()
    caching_ttl_time = IntType()
    gzip_response_type_code = StringType()
    is_secure_token_use = BooleanType()
    secure_token_password = StringType()
    is_access_log_use = BooleanType()
    access_log_file_storage_container_name = StringType()


class GlobalCdnInstance(Model):
    cdn_instance_no = StringType()
    cdn_instance_status = StringType()
    cdn_instance_operation = StringType()
    cdn_instance_status_name = StringType()
    create_date = StringType()
    last_modified_date = StringType()
    cdn_instance_description = StringType()
    #service_name = StringType()
    is_available_partial_domain_purge = BooleanType()
    global_cdn_service_domain_list = ListType(ModelType(CdnPlusServiceDomain))
    global_cdn_rule = ModelType(GlobalCdnRule)