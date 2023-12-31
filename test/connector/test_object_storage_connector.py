import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)
DI = os.environ.get("DOMAIN_ID", None)
PI = os.environ.get('PROJECT_ID', None)

class TestObjectStorageConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK,
        'domain_id': DI,
        'project_id': PI
    }
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.object_storage_connector = ObjectStorageConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_buckets(self):
        list_buckets = self.object_storage_connector.list_buckets()
        print(list_buckets)

    def test_list_objects(self):
        bucket_name = 'my-new-bucket'
        objects = self.object_storage_connector.list_objects(bucket_name)
        print(f"Objects in {bucket_name}:")
        print(objects)

        for obj in objects:
            print(f"Name={obj['Name']}, Size={obj['Size']}, Owner={obj['Owner']}")

    # def test_get_bucket_cors(self):
    #     bucket_name = 'my-new-bucket'
    #     cors_configuration = self.object_storage_connector.get_bucket_cors(bucket_name)
    #     print(f"CORS Configuration for {bucket_name}:")
    #     print(cors_configuration)

    if __name__ == "__main__":
        unittest.main(testRunner=RichTestRunner)


