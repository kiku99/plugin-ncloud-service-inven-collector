from __future__ import print_function
import ncloud_server
from ncloud_server.api.v2_api import V2Api
import logging
from spaceone.core.connector import BaseConnector

__all__ = ['NaverCloudConnector']
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

        secret_data = {
            'ncloud_access_key_id': AKI,
            'ncloud_secret_key': SK
        }
        """

        super().__init__(*args, **kwargs)
        secret_data = kwargs.get('secret_data')

        self.configuration = ncloud_server.Configuration()
        self.configuration.access_key = secret_data['ncloud_access_key_id']
        self.configuration.secret_key = secret_data['ncloud_secret_key']

        self.naverClient = V2Api(ncloud_server.ApiClient(self.configuration))

    def verify(self, **kwargs):
        if self.naverClient is None:
            self.set_connect(**kwargs)


    def generate_query(self, **query):
        query.update({
            'project': 'default'
        })
        return query

