from test.connector.test_object_storage_connector import NCloudObjectStorageConnector

class NCloudObjectStorageManager:

    def __init__(self, access_key=None, secret_key=None):
        self.connector = NCloudObjectStorageConnector(access_key, secret_key)

    def list_buckets(self):
        return self.connector.list_buckets()

    def list_objects(self, bucket_name, prefix=None, delimiter=None, encoding_type=None, max_keys=None, marker=None):
        return self.connector.list_objects(bucket_name, prefix, delimiter, encoding_type, max_keys, marker)

    def get_object(self, bucket_name, object_name, local_file_path):
        return self.connector.get_object(bucket_name, object_name, local_file_path)

    def get_object_acl(self, bucket_name, object_name):
        return self.connector.get_object_acl(bucket_name, object_name)

    def get_bucket_cors(self, bucket_name):
        return self.connector.get_bucket_cors(bucket_name)
