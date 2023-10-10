from spaceone.inventory.libs.connector import NaverCloudConnector
import boto3


__all__ = ['ObjectStorageConnector']


class ObjectStorageConnector:
    def __init__(self, endpoint_url, ncloud_access_key_id, ncloud_secret_access_key):
        self.endpoint_url = endpoint_url
        self.access_key_id = ncloud_access_key_id
        self.secret_access_key = ncloud_secret_access_key
        self.client = self._create_client()

    def _create_client(self):
        return boto3.client('s3',
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key)

    def list_buckets(self):
        response = self.client.list_buckets()
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

        response = self.client.list_objects(Bucket=bucket_name, **params)
        objects = []
        for content in response.get('Contents', []):
            objects.append({
                'Name': content.get('Key'),
                'Size': content.get('Size'),
                'Owner': content.get('Owner').get('ID')
            })
        return objects

    # def get_object_acl(self, bucket_name, object_name):
    #     response = self.client.get_object_acl(Bucket=bucket_name, Key=object_name)
    #     return response

    def get_bucket_cors(self, bucket_name):
        response = self.client.get_bucket_cors(Bucket=bucket_name)
        cors_rules = [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT'],
            'AllowedOrigins': ['*'],
            'MaxAgeSeconds': 3000
        }]
        return response.get('CORSRules', [])