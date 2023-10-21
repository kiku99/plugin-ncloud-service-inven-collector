from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_server
from ncloud_server.rest import ApiException

__all__ = ['ServerConnector']


class ServerConnector(NaverCloudConnector):
    service = 'compute'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_server_instance(self):

        instance_list = []
        get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()

        try:
            api_response = self.server_client.get_server_instance_list(get_server_instance_list_request)
            for instance in api_response.server_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return instance_list

    def list_block_storage_instance(self):
        block_storage_list = []

        get_block_storage_instance_list_request = ncloud_server.GetBlockStorageInstanceListRequest()

        try:
            api_response = self.server_client.get_block_storage_instance_list(get_block_storage_instance_list_request)
            for instance in api_response.block_storage_instance_list:
                block_storage_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return block_storage_list

    def list_login_key(self):
        login_key_list = []
        get_login_key_list_request = ncloud_server.GetLoginKeyListRequest()

        try:
            api_response = self.server_client.get_login_key_list(get_login_key_list_request)
            for instance in api_response.login_key_list:
                login_key_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_login_key_list: %s\n" % e)

        return login_key_list

    def list_init_script(self):
        init_script_list = []
        get_init_script_list_request = ncloud_server.GetInitScriptListRequest()

        try:
            api_response = self.server_client.get_init_script_list(get_init_script_list_request)
            for instance in api_response.init_script_list:
                init_script_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_init_script_list: %s\n" % e)

        return init_script_list

    def list_network_interface(self):
        network_interface_list = []
        get_network_interface_list_request = ncloud_server.GetNetworkInterfaceListRequest()

        try:
            api_response = self.server_client.get_network_interface_list(get_network_interface_list_request)
            for instance in api_response.network_interface_list:
                network_interface_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_network_interface_list: %s\n" % e)

        return network_interface_list
