import unittest
import os
from spaceone.tester import TestCase, print_json
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.inventory.connector.compute.server_connector import ServerConnector
from spaceone.inventory.manager.compute.server.server_instance_manager import ServerInstanceManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestServerInstanceManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'

        cls.server_connector = ServerConnector(secret_data=cls.secret_data)
        cls.server_manager = ServerInstanceManager()
        # cls.server_manager = ServerInstanceManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_Server_Instance(self, *args):
        secret_data = self.secret_data
        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        server_instances = self.server_manager.collect_cloud_service(params)

        for server_instance in server_instances:
            print(server_instance)
            # print(server_instance.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
