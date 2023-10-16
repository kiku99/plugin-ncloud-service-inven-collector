import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.content_delivery.cdn_connector import CdnConnector
AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestCdnConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.cdn_connector = CdnConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_cdn_plus_instance(self):
        cdn_plus_instance = self.cdn_connector.list_cdn_plus_instance()

        print(cdn_plus_instance)

    def test_list_cdn_plus_purge_history_instance(self):
        cdn_plus_purge_history = self.cdn_connector.list_cdn_plus_purge_history_instance(cdnInstanceNo='20015547')

        print(cdn_plus_purge_history)

    def test_list_cdn_global_cdn_instance_instance(self):
        global_cdn_instance = self.cdn_connector.list_cdn_global_cdn_instance_instance()

        print(global_cdn_instance)

    def test_list_global_cdn_purge_history_instance(self):
        global_cdn_purge_history = self.cdn_connector.list_global_cdn_purge_history_instance(cdnInstanceNo='20015547')

        print(global_cdn_purge_history)




if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
