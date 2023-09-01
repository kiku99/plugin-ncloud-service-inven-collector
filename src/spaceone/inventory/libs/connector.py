from __future__ import print_function
import ncloud_server
from ncloud_server.api.v2_api import V2Api
import logging
from spaceone.core.connector import BaseConnector

__all__ = ['NaverCloudConnector']
_LOGGER = logging.getLogger(__name__)


class NaverCloudConnector(BaseConnector):

    def __init__(self, *args: object, **kwargs: object):
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
        self.client = None

    def set_connect(self, secret_data):
        configuration = ncloud_server.Configuration()
        configuration.access_key = secret_data['ncloud_access_key_id']
        configuration.secret_key = secret_data['ncloud_secret_key']

        self.client = V2Api(ncloud_server.ApiClient(configuration))

    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"

    def generate_query(self, **query):
        query.update({
            'project': 'default'
        })
        return query
