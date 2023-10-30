import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.networking.Loadbalancer_connector import LoadbalancerConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestLoadbalancerConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.loadbalacer_connector = LoadbalancerConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_load_balanced_server_instance(self):
        loadbalacer_list = self.loadbalacer_connector.list_load_balanced_server_instance()

        print(loadbalacer_list)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
