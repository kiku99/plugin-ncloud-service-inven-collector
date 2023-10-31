import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.networking.vpc_connector import VpcConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestVpcConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.vpc_connector = VpcConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_vpc(self):
        vpc_list = self.vpc_connector.list_vpc()

        print(vpc_list)

    def test_list_Subnet(self):
        subnet_list = self.vpc_connector.list_Subnet()

        print(subnet_list)

    def test_Network_AclList(self):
        network_acllist = self.vpc_connector.Network_AclList()

        print(network_acllist)

    def test_List_Nat_Gateway_Instance(self):
        get_nat_gateway_instance_list = self.vpc_connector.List_Nat_Gateway_Instance()

        print(get_nat_gateway_instance_list)
    def test_List_Vpc_Peering_Instance(self):
        get_vpc_peering_instance_list = self.vpc_connector.List_Vpc_Peering_Instance()

        print(get_vpc_peering_instance_list)

    def test_List_Route_Table(self):
        get_route_table_list = self.vpc_connector.List_Route_Table()

        print(get_route_table_list)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
