from __future__ import print_function

import ncloud_autoscaling
import ncloud_clouddb
import ncloud_server
import ncloud_monitoring
import ncloud_cdn
import logging
import boto3
from keystoneauth1 import session
from keystoneauth1.identity import v3
import swiftclient
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
        self.object_storage_client = None
        self.archive_storage_client = None
        self.set_connect(kwargs['secret_data'])
        self.object_storage_connect(kwargs['secret_data'])
        self.archive_storage_connect(kwargs['secret_data'])

    def set_connect(self, secret_data: object) -> object:
        configuration_server = ncloud_server.Configuration()
        configuration_server.access_key = secret_data['ncloud_access_key_id']
        configuration_server.secret_key = secret_data['ncloud_secret_key']
        self.server_client = ncloud_server.V2Api(ncloud_server.ApiClient(configuration_server))

        configuration_db = ncloud_clouddb.Configuration()
        configuration_db.access_key = secret_data['ncloud_access_key_id']
        configuration_db.secret_key = secret_data['ncloud_secret_key']
        self.clouddb_client = ncloud_clouddb.V2Api(ncloud_clouddb.ApiClient(configuration_db))

        configuration_autoscaling = ncloud_autoscaling.Configuration()
        configuration_autoscaling.access_key = secret_data['ncloud_access_key_id']
        configuration_autoscaling.secret_key = secret_data['ncloud_secret_key']
        self.autoscaling_client = ncloud_autoscaling.V2Api(ncloud_autoscaling.ApiClient(configuration_autoscaling))

        configuration_monitoring = ncloud_monitoring.Configuration()
        configuration_monitoring.access_key = secret_data['ncloud_access_key_id']
        configuration_monitoring.secret_key = secret_data['ncloud_secret_key']
        self.monitoring_client = ncloud_monitoring.V2Api(ncloud_monitoring.ApiClient(configuration_monitoring))

        configuration_cdn = ncloud_cdn.Configuration()
        configuration_cdn.access_key = secret_data['ncloud_access_key_id']
        configuration_cdn.secret_key = secret_data['ncloud_secret_key']
        self.cdn_client = ncloud_cdn.V2Api(ncloud_cdn.ApiClient(configuration_cdn))

    def object_storage_connect(self, secret_data: object) -> object:
        object_endpoint_url = 'https://kr.object.ncloudstorage.com'
        object_storage_access_key = secret_data['ncloud_access_key_id']
        object_storage_secret_key = secret_data['ncloud_secret_key']
        self.object_storage_client = boto3.client(service_name='s3',
                                                  endpoint_url=object_endpoint_url,
                                                  aws_access_key_id=object_storage_access_key,
                                                  aws_secret_access_key=object_storage_secret_key
                                                  )
    def archive_storage_connect(self, secret_data: object) -> object:
        archive_endpoint_url = 'https://kr.archive.ncloudstorage.com:5000/v3'
        archive_storage_access_key = secret_data['ncloud_access_key_id']
        archive_storage_secret_key = secret_data['ncloud_secret_key']
        #사용자 정의
        domain_id = 'default'
        project_id = 'abfdc070c4144ce789a59559c8f3e55e'
        auth = v3.Password(auth_url=archive_endpoint_url,
                                                  username=archive_storage_access_key,
                                                  password=archive_storage_secret_key,
                                                  project_id=project_id,
                                                  user_domain_id=domain_id)
        auth_session = session.Session(auth=auth)
        self.archive_storage_client = swiftclient.Connection(retries=5, session=auth_session)

    def verify(self, **kwargs):
        if self.server_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"

        if self.clouddb_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"

        if self.object_storage_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"
