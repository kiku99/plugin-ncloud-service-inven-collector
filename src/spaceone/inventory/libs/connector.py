from __future__ import print_function

import ncloud_autoscaling
import ncloud_clouddb
import ncloud_server
from ncloud_server.api.v2_api import V2Api
import logging
from spaceone.core.connector import BaseConnector

__all__ = ['NaverCloudConnector']

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA = 'naver_client_secret'


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
        self.server_client = None
        self.clouddb_client = None
        self.autoscaling_client = None
        self.set_connect(kwargs['secret_data'])

    def set_connect(self, secret_data: object) -> object:
        configuration_server = ncloud_server.Configuration()
        configuration_server.access_key = secret_data['ncloud_access_key_id']
        configuration_server.secret_key = secret_data['ncloud_secret_key']
        self.server_client = V2Api(ncloud_server.ApiClient(configuration_server))

        configuration_db = ncloud_clouddb.Configuration()
        configuration_db.access_key = secret_data['ncloud_access_key_id']
        configuration_db.secret_key = secret_data['ncloud_secret_key']
        self.clouddb_client = V2Api(ncloud_clouddb.ApiClient(configuration_db))

        configuration_autoscaling = ncloud_autoscaling.Configuration()
        configuration_autoscaling.access_key = secret_data['ncloud_access_key_id']
        configuration_autoscaling.secret_key = secret_data['ncloud_secret_key']
        self.autoscaling_client = V2Api(ncloud_autoscaling.ApiClient(configuration_autoscaling))


    def verify(self, **kwargs):
        if self.server_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"

        if self.clouddb_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"
