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


class S3Client:
    def __init__(self, endpoint_url, region_name, access_key, secret_key):
        self.s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

    def list_buckets(self):
        response = self.s3.list_buckets()
        for bucket in response.get('Buckets', []):
            print(bucket.get('Name'))

    def put_bucket(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def delete_bucket(self, bucket_name):
        self.s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted successfully.")

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

    def list_top_level_objects(self, bucket_name, delimiter=None, max_keys=None):
        self.list_objects(bucket_name, delimiter=delimiter, max_keys=max_keys)

    def put_object(self, bucket_name, object_name, data):
        md5_hash = hashlib.md5(data).digest()
        base64_md5_hash = base64.b64encode(md5_hash).decode('utf-8')

        response = self.s3.put_object(Bucket=bucket_name, Key=object_name, Body=data, ContentMD5=base64_md5_hash)
        print(f'Object "{object_name}" uploaded successfully.')

    def get_object(self, bucket_name, object_name, local_file_path):
        self.s3.download_file(bucket_name, object_name, local_file_path)
        print(f'Object "{object_name}" downloaded to "{local_file_path}".')

    def delete_object(self, bucket_name, object_name):
        self.s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f'Object "{object_name}" deleted successfully.')

    def set_bucket_acl(self, bucket_name, acl):
        # ACL 값: 'private', 'public-read', 'public-read-write', 'authenticated-read', 등
        self.s3.put_bucket_acl(Bucket=bucket_name, ACL=acl)
        print(f'Bucket ACL set to "{acl}".')

        response = self.s3.get_bucket_acl(Bucket=bucket_name)
        print(f'Completion of bucket acl')

    # ACL 생성 얘 안됨
    # def set_object_acl(self, bucket_name, object_name, owner_id, target_id, permission):
    #     self.s3.put_object_acl(Bucket=bucket_name, Key=object_name,
    #                           AccessControlPolicy={
    #                               'Grants': [
    #                                   {
    #                                       'Grantee': {
    #                                           'ID': owner_id,
    #                                           'Type': 'CanonicalUser'
    #                                       },
    #                                       'Permission': 'FULL_CONTROL'
    #                                   },
    #                                   {
    #                                       'Grantee': {
    #                                           'ID': target_id,
    #                                           'Type': 'CanonicalUser'
    #                                       },
    #                                       'Permission': 'READ'
    #                                   }
    #                               ],
    #                               'Owner': {
    #                                   'ID': owner_id
    #                               }
    #                           })
    #     response = self.s3.get_object_acl(Bucket=bucket_name, Key=object_name)

    def get_object_acl(self, bucket_name, object_name):
        response = self.s3.get_object_acl(Bucket=bucket_name, Key=object_name)
        return response

    def upload_large_object(self, bucket_name, object_name, local_file):
        # Initialize and get upload ID
        create_multipart_upload_response = self.s3.create_multipart_upload(Bucket=bucket_name, Key=object_name)
        upload_id = create_multipart_upload_response['UploadId']

        part_size = 10 * 1024 * 1024  # 10 MB
        parts = []

        try:
            # Upload parts
            with open(local_file, 'rb') as f:
                part_number = 1
                while True:
                    data = f.read(part_size)
                    if not len(data):
                        break
                    upload_part_response = self.s3.upload_part(
                        Bucket=bucket_name,
                        Key=object_name,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=data
                    )
                    parts.append({
                        'PartNumber': part_number,
                        'ETag': upload_part_response['ETag']
                    })
                    part_number += 1

            # Complete multipart upload
            multipart_upload = {'Parts': parts}
            self.s3.complete_multipart_upload(
                Bucket=bucket_name,
                Key=object_name,
                UploadId=upload_id,
                MultipartUpload=multipart_upload
            )

            print(f'Large object "{object_name}" uploaded successfully.')

        except Exception as e:
            print(f'Error uploading large object: {e}')
            # If there is an error, abort the multipart upload
            self.s3.abort_multipart_upload(
                Bucket=bucket_name,
                Key=object_name,
                UploadId=upload_id
            )
            print(f'Multipart upload for "{object_name}" aborted.')

    def put_bucket_cors(self, bucket_name, cors_rules):
        cors_configuration = {
            'CORSRules': cors_rules
        }
        self.s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)

    def get_bucket_cors(self, bucket_name):
        response = self.s3.get_bucket_cors(Bucket=bucket_name)
        return response.get('CORSRules', [])

if __name__ == "__main__":
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'

    s3_client = S3Client(endpoint_url, region_name, AKI, SK)

    s3_client.list_buckets()

    bucket_name = 'my-new-bucket'

    s3_client.put_bucket(bucket_name)
    s3_client.delete_bucket(bucket_name)

    s3_client.list_objects(bucket_name)
    s3_client.list_top_level_objects(bucket_name)

    object_name = 'sample-object'
    data_to_upload = b'This is the content of the uploaded object.'
    s3_client.put_object(bucket_name, object_name, data_to_upload)

    local_file_path = '/tmp/test.txt'
    s3_client.get_object(bucket_name, object_name, local_file_path)

    s3_client.delete_object(bucket_name, object_name)

    # 버킷 ACL 설정
    bucket_acl = 'public-read'
    s3_client.set_bucket_acl(bucket_name, bucket_acl)

    # 오브젝트 ACL 설정
    # 얘 안됨
    owner_id = 'test-owner-id'
    target_id = 'test-user-id'
    permission = 'READ'
    #s3_client.set_object_acl(bucket_name, object_name, owner_id, target_id, permission)
    #acl_response = s3_client.get_object_acl(bucket_name, object_name)
    #print('Object ACL:', acl_response)

    local_file = '/tmp/test.txt'
    s3_client.upload_large_object(bucket_name, object_name, local_file)

    # Define CORS rules
    cors_rules = [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'PUT'],
        'AllowedOrigins': ['*'],
        'MaxAgeSeconds': 3000
    }]

    # Set CORS configuration
    s3_client.put_bucket_cors(bucket_name, cors_rules)

    # Get CORS configuration
    cors_configuration = s3_client.get_bucket_cors(bucket_name)
    print(cors_configuration)