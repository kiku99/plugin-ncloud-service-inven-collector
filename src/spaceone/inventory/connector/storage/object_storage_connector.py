from spaceone.inventory.libs.connector import NaverCloudConnector
import boto3

__all__ = ['ObjectStorageConnector']

config = boto3.session.Config(signature_version='s3v4')

class ObjectStorageConnector(NaverCloudConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_buckets(self):
        response = self.object_storage_client.list_buckets()
        return response

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

        response = self.object_storage_client.list_objects(Bucket=bucket_name, **params)
        objects = []
        for content in response.get('Contents', []):
            objects.append({
                'Name': content.get('Key'),
                'Size': content.get('Size'),
                'Owner': content.get('Owner').get('ID')
            })
        return objects

    def get_bucket_cors(self, bucket_name):
        response = self.object_storage_client.get_bucket_cors(Bucket=bucket_name)
        return response