import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.content_delivery.cdn_connector import CdnConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.content_delivery.cdn.data import CdnPlusInstance, CdnPlusRule, CdnPlusServiceDomain
from spaceone.inventory.model.content_delivery.cdn.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.content_delivery.cdn.cloud_service import CdnResource, CdnResponse
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class CdnManager(NaverCloudManager):
    connector_name = 'CdnConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[CdnResponse], List[CdnResource]]:
        _LOGGER.debug(f'** Cdn START **')
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        resource_responses = []
        error_responses = []
        start_time = time.time()

        ##################################
        # 0. Gather All Related Resources
        ##################################
        self.instance_conn: CdnConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])

        cdn_plus_instance_list = self.instance_conn.list_cdn_plus_instance()
        cdn_plus_pluge_history_list = self.instance_conn.list_cdn_plus_purge_history_instance(params['cdnInstanceNo'])

        global_cdn_instance_list = self.instance_conn.list_cdn_global_cdn_instance_instance()
        global_cdn_purge_history_list = self.instance_conn.list_global_cdn_purge_history_instance(params['cdnInstanceNo'])

        #metirc_statistic_list = self.instance_conn.list_metric_statistic(params["instance_no"], params["metric_name"], params["period"], params["start_time"], params["end_time"])

        for instance in cdn_plus_instance_list:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                instance_no = instance.cdn_instance_no
                instance_rule = instance.cdn_plus_rule
                instance_create_date = instance.create_date
                instance_service_domain_list = instance.cdn_plus_service_domain_list
                cdn_plus_rule = self._get_cdn_plus_rule(instance_rule)
                cdn_plus_service_domain_list = self._get_cdn_plus_service_domain(instance_service_domain_list)
                instance_info = {

                    'cdn_instance_status': instance.cdn_instance_status.code,
                    'cdn_instance_operation': instance.cdn_instance_operation.code,
                    'cdn_instance_status_name': instance.cdn_instance_status_name,
                    'last_modified_date': instance.last_modified_date,
                    'service_name': instance.service_name,
                    'is_for_live_transcoder': instance.is_for_live_transcoder,
                    'is_for_image_optimizer': instance.is_for_image_optimizer,
                    'is_available_partial_domain_purge': instance.is_available_partial_domain_purge,
                    'cdn_plus_service_domain_list': cdn_plus_service_domain_list,
                    'cdn_plus_rule': cdn_plus_rule,


                }
                ##################################
                # 2. Make Base Data
                ##################################
                cdn_plus_instance = CdnPlusInstance(instance_info, strict=False)



                ##################################
                # 3. Make Return Resource
                ##################################
                monitoring_resource = CdnResource({
                    'name': instance_no,
                    'launched_at': instance_create_date,
                    'data': cdn_plus_instance
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(CdnResponse({'resource': monitoring_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] cdn_instance_no => {instance.cdn_instance_no}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'content_delivery', 'cdn', instance_no)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_cdn_plus_service_domain(serivice_list):
        # Convert database list(dict) -> list(database object)
        cdn_plus_service_list = []
        for service in serivice_list:
            service_data = {
                'domain_id': service.domain_id,
                'service_domain_type_code': service.service_domain_type_code,
                'protocol_type_code': service.protocol_type_code,
                'default_domain_name': service.default_domain_name,
                'user_domain_name': service.user_domain_name,
            }
            cdn_plus_service_list.append(service_data)

        return cdn_plus_service_list

    @staticmethod
    def _get_cdn_plus_rule(instance):
        # Convert database list(dict) -> list(database object)
        cdn_plus_rule_list = []
        rule_data = {
                'protocol_type_code': instance.protocol_type_code,
                'service_domain_type_code': instance.service_domain_type_code,
                'origin_url': instance.origin_url,
                'origin_http_port': instance.origin_http_port,
                'origin_https_port': instance.origin_https_port,
                'forward_host_header_type_code': instance.forward_host_header_type_code,
                'cache_key_host_name_type_code': instance.cache_key_host_name_type_code,
                'caching_option_type_code': instance.caching_option_type_code,
                'caching_ttl_time': instance.caching_ttl_time,
                'gzip_response_type_code': instance.gzip_response_type_code,
                'is_access_log_use': instance.is_access_log_use,
                'is_error_contents_response_use': instance.is_error_contents_response_use,
                'is_gzip_compression_use': instance.is_gzip_compression_use,
                'is_large_file_optimization_use': instance.is_large_file_optimization_use,
                'is_query_string_ignore_use': instance.is_query_string_ignore_use,
                'is_referrer_domain_restrict_use': instance.is_referrer_domain_restrict_use,
                'is_referrer_domain_use': instance.is_referrer_domain_use,
                'is_reissue_secure_token_password': instance.is_reissue_secure_token_password,

            }
        cdn_plus_rule_list.append(rule_data)

        return cdn_plus_rule_list

    #
    # @staticmethod
    # def _get_matched_cdn_plus_purge_history(instance, cdn_plus_pluge_history_list):
    #     # Convert database list(dict) -> list(database object)
    #     purge_history_list = []
    #     for service in instance:
    #         service_data = {
    #             'domain_id': service.domain_id,
    #             'service_domain_type_code': service.service_domain_type_code,
    #             'protocol_type_code': service.protocol_type_code,
    #             'default_domain_name': service.default_domain_name,
    #             'user_domain_name': service.user_domain_name,
    #         }
    #         purge_history_list.append(service_data)
    #
    #     return purge_history_list


