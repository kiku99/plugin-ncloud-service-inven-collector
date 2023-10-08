import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestCloudDBInstanceConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.cloud_db_connector = CloudDBConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_cloud_db_instance(self):
        cloud_db_instances = self.cloud_db_connector.list_cloud_db_instance("MYSQL")

        print(cloud_db_instances)

    def test_list_object_storage_backup_instance(self):
        storage_backup_instances = self.cloud_db_connector.list_object_storage_backup(1057304, "/")

        print(storage_backup_instances)

    def test_list_backup(self):
        back_up = self.cloud_db_connector.list_backup(1057304)

        print(back_up)

    def test_list_product(self):
        product = self.cloud_db_connector.list_product(self.cloud_db_connector.list_img_product("MSSQL"))

        print(product)

    def test_list_dms_operation(self):
        operation = self.cloud_db_connector.list_dms_operation(782063)

        print(operation)

    def test_list_img_product(self):
        img_product = self.cloud_db_connector.list_img_product("MSSQL")

        print(img_product)

    def test_list_config_group(self):
        group = self.cloud_db_connector.list_config_group("MSSQL")

        print(group)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
