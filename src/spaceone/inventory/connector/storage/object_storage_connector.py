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

    # {'ResponseMetadata': {'RequestId': '1d7a642b-d071-46cf-8647-282a3cfc7f6e', 'HostId': '', 'HTTPStatusCode': 200,
    #                       'HTTPHeaders': {'date': 'Thu, 19 Oct 2023 11:23:12 GMT',
    #                                       'x-clv-request-id': '1d7a642b-d071-46cf-8647-282a3cfc7f6e',
    #                                       'x-clv-s3-version': '2.5', 'accept-ranges': 'bytes',
    #                                       'x-amz-request-id': '1d7a642b-d071-46cf-8647-282a3cfc7f6e',
    #                                       'content-type': 'application/xml', 'content-length': '625'},
    #                       'RetryAttempts': 0},
    #  'Buckets': [
    #     {'Name': 'bucket-a', 'CreationDate': datetime.datetime(2023, 10, 6, 9, 44, 16, 187000, tzinfo=tzutc())},
    #     {'Name': 'bucket-b', 'CreationDate': datetime.datetime(2023, 10, 8, 15, 23, 46, 377000, tzinfo=tzutc())},
    #     {'Name': 'my-new-bucket', 'CreationDate': datetime.datetime(2023, 10, 8, 15, 40, 39, 25000, tzinfo=tzutc())},
    #     {'Name': 'your-bucket-name', 'CreationDate': datetime.datetime(2023, 10, 10, 16, 2, 31, 647000, tzinfo=tzutc())}],
    #  'Owner': {'DisplayName': 'ncp-3040466-0', 'ID': 'ncp-3040466-0'}}




