import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector
import boto3

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestObjectStorageConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        ncloud_access_key_id = os.environ.get('NCLOUD_ACCESS_KEY_ID')
        ncloud_secret_key = os.environ.get('NCLOUD_SECRET_KEY')

        if ncloud_access_key_id and ncloud_secret_key:
            cls.object_storage_connector = ObjectStorageConnector(
                endpoint_url='https://kr.object.ncloudstorage.com',
                ncloud_access_key_id=ncloud_access_key_id,
                ncloud_secret_access_key=ncloud_secret_key
            )
        else:
            raise ValueError("NCLOUD_ACCESS_KEY_ID and NCLOUD_SECRET_KEY environment variables are not set.")

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_buckets(self):
        list_buckets = self.object_storage_connector.list_buckets()
        print(list_buckets)
        #for bucket in list_buckets:
        #    print(bucket)

    def test_list_objects(self):
        bucket_name = 'my-new-bucket'
        objects = self.object_storage_connector.list_objects(bucket_name)
        print(f"Objects in {bucket_name}:")
        for obj in objects:
            print(f"Name={obj['Name']}, Size={obj['Size']}, Owner={obj['Owner']}")

    # def test_get_object_acl(self):
    #     bucket_name = 'your-bucket-name'
    #     object_name = 'your-object-key'
    #     acl = self.object_storage_connector.get_object_acl(bucket_name, object_name)
    #     print(f"ACL for {object_name}:")
    #     print(acl)

    def test_get_bucket_cors(self):
        bucket_name = 'my-new-bucket'
        cors_configuration = self.object_storage_connector.get_bucket_cors(bucket_name)
        print(f"CORS Configuration for {bucket_name}:")
        print(cors_configuration)

    if __name__ == "__main__":
        unittest.main(testRunner=RichTestRunner)
