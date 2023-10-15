import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector
from spaceone.inventory.manager.storage.object_storage_manager import ObjectStorageManager

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
        cls.object_storage_connector = ObjectStorageConnector(
                    endpoint_url='https://kr.object.ncloudstorage.com',
                    ncloud_access_key_id = cls.secret_data['ncloud_access_key_id'],
                    ncloud_secret_access_key=cls.secret_data['ncloud_secret_key']
                )
        cls.object_storage_manager = ObjectStorageManager()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_object_storage_manager(self):
        secret_data = self.secret_data
        params = {'option': {},'secret_data': secret_data, 'filter': {}, 'bucket_name':"bucket-a"}

        object_storage_instances = self.object_storage_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(object_storage_instances[0][0].to_primitive())

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)


