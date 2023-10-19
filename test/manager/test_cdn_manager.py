import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.content_delivery.cdn_connector import CdnConnector
from spaceone.inventory.manager.content_delivery.cdn.cdn_manager import CdnManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestCdnManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'

        cls.cdn_connector = CdnConnector(secret_data=cls.secret_data)
        cls.cdn_manager = CdnManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_server_instance_manager(self):
        secret_data = self.secret_data

        params = {'option': {}, 'secret_data': secret_data, 'filter': {}, 'cdnInstanceNo': '20015547'}

        cdn_instance = self.cdn_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(cdn_instance[0][0].to_primitive())

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
