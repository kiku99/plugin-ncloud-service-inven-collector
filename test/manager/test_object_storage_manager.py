import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector
from spaceone.inventory.manager.storage.object_storage.object_storage_manager import ObjectStorageManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestObjectStorageManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.object_storage_connector = ObjectStorageConnector(secret_data=cls.secret_data)
        cls.object_storage_manager = ObjectStorageManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_object_storage_manager(self):
        secret_data = self.secret_data
        params = {'secret_data': secret_data, 'bucket_name':"my-new-bucket"}
        object_storage_instances = self.object_storage_manager.collect_cloud_service(params)

        print(object_storage_instances[0][3].to_primitive())

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)


