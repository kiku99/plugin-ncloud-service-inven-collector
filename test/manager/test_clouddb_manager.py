import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector
from spaceone.inventory.manager.database.cloud_db.cloud_db_manager import CloudDBManager

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

        cls.cloud_db_connector = CloudDBConnector(secret_data=cls.secret_data)
        cls.cloud_db_manager = CloudDBManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_server_instance_manager(self):
        secret_data = self.secret_data
        options = {'dbKindCode': "MYSQL",
                   "cloudDBImageProductCode": "SPSWMSSQLWINNT01"
                   # "cloud_db_instance_no": "1057304",
                   # "cloud_db_image_product_code": "SPSWMSSQLWINNT01",
                   # "folderName": "/",
                   # "requestNo": "782063"
                   }
        params = {'options': options, 'secret_data': secret_data, 'filter': {}}

        server_instances = self.cloud_db_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(server_instances[0][0].to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
