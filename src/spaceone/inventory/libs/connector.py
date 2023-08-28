from __future__ import print_function
import ncloud_server
from ncloud_server.rest import ApiException
import ncloud_apikey
import logging

from spaceone.core.connector import BaseConnector

_DEFAULT_SCHEMA = 'naver_cloud_oauth_client_id'
_LOGGER = logging.getLogger(__name__)

class NaverCloudConnector(BaseConnector):
    naver_client_service = 'compute'
    version = 'v2'

    def __init__(self, *args, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data

        secret_data(dict)
            - type: ..
            - access_key: ...
            - secret_key: ...
            - ...
        """

        super().__init__(*args, **kwargs)
        secret_data = kwargs.get('secret_data')

        # create an instance of the API class
       # configuration = ncloud_server.Configuration()
        #configuration.access_key = "access_key"

        #configuration.secret_key = "secret_key"


        self.credentials = ncloud_apikey.Credentials

        self.client = ncloud_server.V2Api(ncloud_server.ApiClient(credentials=self.credentials))
        get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()
        #add_nas_volume_access_control_request = ncloud_server.AddNasVolumeAccessControlRequest()  # AddNasVolumeAccessControlRequest | addNasVolumeAccessControlRequest

        try:
            api_response = self.client.get_server_instance_list(get_server_instance_list_request)
            print(api_response)
        except ApiException as e:
            print("Exception when calling V2Api->add_nas_volume_access_control: %s\n" % e)


    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(**kwargs)

    def generate_query(self, **query):
        query.update({
            'project': self.project_id,
        })
        return query

    def list_zones(self, **query):
        query = self.generate_query(**query)
        result = self.client.zones().list(**query).execute()
        return result.get('items', [])
