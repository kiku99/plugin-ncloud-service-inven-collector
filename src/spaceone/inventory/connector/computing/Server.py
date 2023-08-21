from src.spaceone.inventory.libs.connector import NaverCloudConnector
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

class Server(NaverCloudConnector):
    Naver_client_service = 'compute'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getRegion(self):
        api_instance = V2Api(ncloud_server.ApiClient(configuration))


#
# configuration = ncloud_server.Configuration()
#
#
# configuration.access_key = 'JTzqj1cN0fd3mIegCEI8'
# configuration.secret_key = 'GcnavhhuQHzZ7kGjDdyAQz6OSgIW2N0Z3Y0LSuFM'
#
# api_instance = V2Api(ncloud_server.ApiClient(configuration))
# get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()
# ## get_login_key_list_request = ncloud_server.GetLoginKeyListRequest()
#
#
# try:
#     ## api_response = api_instance.get_login_key_list(get_login_key_list_request)
#     api_response = api_instance.get_server_instance_list(get_server_instance_list_request)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling V2Api->get_login_key_list: %s\n" % e)