from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_server
from ncloud_server.rest import ApiException

__all__ = ['ServerConnector']


class ServerConnector(NaverCloudConnector):
    service = 'compute'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_Server_Instance(self):

        instance_list = []
        get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()

        try:
            api_response = self.client.get_server_instance_list(get_server_instance_list_request)
            # print(api_response)
            for instance in api_response.server_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return instance_list

    def list_Storage_Instance(self):
        storage_list = []

        get_block_storage_instance_list_request = ncloud_server.GetBlockStorageInstanceListRequest()

        try:
            api_response = self.client.get_block_storage_instance_list(get_block_storage_instance_list_request)
            for instance in api_response.block_storage_instance_list:
                storage_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return storage_list

    def list_login_key(self):
        login_key_list = []
        get_login_key_list_request = ncloud_server.GetLoginKeyListRequest()

        try:
            api_response = self.client.get_login_key_list(get_login_key_list_request)
            for instance in api_response.login_key_list:
                login_key_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return login_key_list
