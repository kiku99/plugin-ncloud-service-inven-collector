import base64
import hashlib
import os
import boto3
from lxml import etree as ET

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)

if AKI is None or SK is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your NCloud credential first for test

        ##################################################
        example)

        export NAVER_APPLICATION_CREDENTIALS="<PATH>" 
    """)
    exit


class TestObjectStorageConnector:
    def __init__(self, endpoint_url, region_name, access_key, secret_key):
        self.s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

    def list_buckets(self):
        response = self.s3.list_buckets()
        for bucket in response.get('Buckets', []):
            print(bucket.get('Name'))

    def list_objects(self, bucket_name, prefix=None, delimiter=None, encoding_type=None, max_keys=None, marker=None):
        params = {}
        if prefix:
            params['Prefix'] = prefix
        if delimiter:
            params['Delimiter'] = delimiter
        if encoding_type:
            params['EncodingType'] = encoding_type
        if max_keys:
            params['MaxKeys'] = max_keys
        if marker:
            params['Marker'] = marker

        response = self.s3.list_objects(Bucket=bucket_name, **params)

        print(f'Object List in Bucket "{bucket_name}":')

        for content in response.get('Contents', []):
            print(f' Name={content.get("Key")}, Size={content.get("Size")}, Owner={content.get("Owner").get("ID")}')

        if response.get('IsTruncated'):
            self.list_objects(bucket_name, prefix, delimiter, encoding_type, max_keys, response.get('NextMarker'))

    # def list_top_level_objects(self, bucket_name, delimiter=None, max_keys=None):
    #     self.list_objects(bucket_name, delimiter=delimiter, max_keys=max_keys)

    def get_object(self, bucket_name, object_name, local_file_path):
        self.s3.download_file(bucket_name, object_name, local_file_path)
        print(f'Object "{object_name}" downloaded to "{local_file_path}".')

    def get_object_acl(self, bucket_name, object_name):
        response = self.s3.get_object_acl(Bucket=bucket_name, Key=object_name)
        return response

    def get_bucket_cors(self, bucket_name):
        response = self.s3.get_bucket_cors(Bucket=bucket_name)
        return response.get('CORSRules', [])


if __name__ == "__main__":
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'
    s3_client = TestObjectStorageConnector(endpoint_url, region_name, AKI, SK)
    s3_client.list_buckets()

    bucket_name = 'my-new-bucket'
    object_name = 'sample-object'
    local_file_path = '/tmp/test.txt'

    s3_client.list_objects(bucket_name)
    # s3_client.list_top_level_objects(bucket_name)
    s3_client.get_object(bucket_name, object_name, local_file_path)

    # Define CORS rules
    cors_rules = [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'PUT'],
        'AllowedOrigins': ['*'],
        'MaxAgeSeconds': 3000
    }]

    # Get CORS configuration
    cors_configuration = s3_client.get_bucket_cors(bucket_name)
    print(cors_configuration)