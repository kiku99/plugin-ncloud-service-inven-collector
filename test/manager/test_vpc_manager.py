import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.networking.vpc_connector import VpcConnector
from spaceone.inventory.manager.networking.VPC.vpc_network_manager import VPCNetworkManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestVpcManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'

        cls.vpc_connector = VpcConnector(secret_data=cls.secret_data)
        cls.vpc_manager = VPCNetworkManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_vpc_manager(self):
        secret_data = self.secret_data
        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        vpc_network = self.vpc_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(vpc_network[0][0].to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
