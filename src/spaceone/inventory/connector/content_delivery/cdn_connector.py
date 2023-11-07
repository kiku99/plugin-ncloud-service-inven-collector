from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_cdn
from ncloud_clouddb.rest import ApiException

__all__ = ['CdnConnector']


class CdnConnector(NaverCloudConnector):
    service = 'Cdn'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_cdn_plus_instance(self):

        cdn_plus_instance_list = []
        get_cdn_plus_instance_list_request = ncloud_cdn.GetCdnPlusInstanceListRequest()

        try:
            api_response = self.cdn_client.get_cdn_plus_instance_list(get_cdn_plus_instance_list_request)
            # print(api_response)
            for instance in api_response.cdn_plus_instance_list:
                cdn_plus_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cdn_plus_instance_list: %s\n" % e)

        return cdn_plus_instance_list


    def list_cdn_plus_purge_history_instance(self, cdn_instance_no):

        cdn_plus_purge_history_list = []
        get_cdn_plus_purge_history_list_request = ncloud_cdn.GetCdnPlusPurgeHistoryListRequest(cdn_instance_no=cdn_instance_no)

        try:
            api_response = self.cdn_client.get_cdn_plus_purge_history_list(get_cdn_plus_purge_history_list_request)
            # print(api_response)
            for instance in api_response.cdn_plus_purge_history_list:
                cdn_plus_purge_history_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cdn_plus_purge_history_list: %s\n" % e)

        return cdn_plus_purge_history_list

    def list_cdn_global_cdn_instance_instance(self):

        global_cdn_instance_list = []
        get_global_cdn_instance_list_request = ncloud_cdn.GetGlobalCdnInstanceListRequest()

        try:
            api_response = self.cdn_client.get_global_cdn_instance_list(get_global_cdn_instance_list_request)
            # print(api_response)
            for instance in api_response.global_cdn_instance_list:
                global_cdn_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_global_cdn_instance_list: %s\n" % e)

        return global_cdn_instance_list

    def list_global_cdn_purge_history_instance(self, cdn_instance_no):

        global_cdn_purge_history_list = []
        get_global_cdn_purge_history_list_request = ncloud_cdn.GetGlobalCdnPurgeHistoryListRequest(cdn_instance_no=cdn_instance_no)

        try:
            api_response = self.cdn_client.get_global_cdn_purge_history_list(get_global_cdn_purge_history_list_request)
            # print(api_response)
            for instance in api_response.global_cdn_purge_history_list:
                global_cdn_purge_history_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_global_cdn_purge_history_list: %s\n" % e)

        return global_cdn_purge_history_list



