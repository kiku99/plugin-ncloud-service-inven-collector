import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.archive_storage_connector import ArchiveStorageConnector
from spaceone.inventory.manager.storage.archive_storage_manager import ArchiveStorageManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestArchiveStorageManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.archive_storage_connector = ArchiveStorageConnector(secret_data=cls.secret_data)
        cls.archive_storage_manager = ArchiveStorageManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_archive_storage_manager(self):
        secret_data = self.secret_data
        params = {'secret_data': secret_data, 'bucket_name':"sample-container"}

        archive_storage_instances = self.archive_storage_manager.collect_cloud_service(params)

        print(archive_storage_instances[0][0].to_primitive())

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)