from __future__ import print_function
import ncloud_server


from spaceone.core.connector import BaseConnector

class NaverCloudConnector(BaseConnector):
    Naver_client_service = 'compute'
    version = 'v2'

    def __init__(self, *args, **kwargs):
        """
        kwargs
            - access_key
            - secret_key
        """

        super().__init__(*args, **kwargs)
        configuration = ncloud_server.Configuration()
        configuration.access_key = kwargs.get('access_key')

        configuration.secret_key = kwargs.get('secret_key')
        self.project_id = secret_data.get('project_id')

    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(**kwargs)

    # def generate_query(self, **query):
    #     query.update({
    #         'project': self.project_id,
    #     })
    #     return query
    #
    # def list_zones(self, **query):
    #     query = self.generate_query(**query)
    #     result = self.client.zones().list(**query).execute()
    #     return result.get('items', [])