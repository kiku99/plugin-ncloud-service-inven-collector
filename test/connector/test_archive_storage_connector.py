import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.archive_storage_connector import ArchiveStorageConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestObjectStorageConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.archive_storage_connector = ArchiveStorageConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_buckets(self):
        list_buckets = self.archive_storage_connector.list_buckets()
        print(list_buckets)

    def test_list_objects(self):
        container_name = 'sample-container'
        list_objects = self.archive_storage_connector.list_objects(container_name)
        print(list_objects)

