from __future__ import print_function
import ncloud_server
import ncloud_vpc
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
        self.client = None
        self.vpc_client = None
        self.set_connect(kwargs['secret_data'])

    def set_connect(self, secret_data: object) -> object:
        configuration = ncloud_server.Configuration()
        configuration.access_key = secret_data['ncloud_access_key_id']
        configuration.secret_key = secret_data['ncloud_secret_key']
        self.client = V2Api(ncloud_server.ApiClient(configuration))

        configuration_vpc = ncloud_vpc.Configuration()
        configuration_vpc.access_key = secret_data['ncloud_access_key_id']
        configuration_vpc.secret_key = secret_data['ncloud_secret_key']
        self.vpc_client = ncloud_vpc.V2Api(ncloud_vpc.ApiClient(configuration_vpc))

    def verify(self, **kwargs):
        if self.client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"
        if self.vpc_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"
