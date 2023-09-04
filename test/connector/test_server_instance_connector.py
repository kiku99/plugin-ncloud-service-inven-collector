import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.compute.server_connector import ServerConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestLoadBalancerConnector(unittest.TestCase):
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

    def test_list_load_balancers(self):
        server_instances = self.server_connector.list_Server_Instance()

        print(server_instances)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)