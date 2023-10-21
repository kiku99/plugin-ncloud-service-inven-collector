import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.compute.server_connector import ServerConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestServerInstanceConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.server_connector = ServerConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_server_instance(self):
        server_instances = self.server_connector.list_server_instance()

        print(server_instances)

    def test_list_storage_instance(self):
        storage_instances = self.server_connector.list_block_storage_instance()

        print(storage_instances)

    def test_list_login_key(self):
        login_key = self.server_connector.list_login_key()

        print(login_key)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
