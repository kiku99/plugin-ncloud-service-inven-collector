import time
import logging
from typing import Tuple, List

from datetime import datetime, timedelta
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.storage.archive_storage_connector import ArchiveStorageConnector
from spaceone.inventory.model.storage.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.cloud_service import ArchiveStorageResource, ArchiveStorageResponse
from spaceone.inventory.model.storage.data import ArchiveBucketGroup
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class ArchiveStorageManager(NaverCloudManager):
    connector_name = 'ArchiveStorageConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[ArchiveStorageResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** Storage START **')
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse/ErrorResourceResponse
        """
        resource_responses = []
        error_responses = []
        start_time = time.time()
        bucket_dict = {}

        #################################
        # 0. Gather All Related Resources
        ##################################
        self.instance_conn: ArchiveStorageConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.archive_storage_connect(params['secret_data'])

        buckets = self.instance_conn.list_buckets()
        objects = self.instance_conn.list_objects(params['bucket_name'])

        # Buckets 형태를 list->dict로 바꾸기
        # convert_buckets_to_dict(buckets, bucket_dict)

        print("시작")
        for bucket_group in buckets:
            print(bucket_group)

        for bucket_group in buckets:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################

                data = {
                    'ResponseMetadata': {
                        'request_id': buckets['ResponseMetadata']['RequestId'],
                        'host_id': buckets['ResponseMetadata']['HostId'],
                        'http_statuscode': buckets['ResponseMetadata']['HTTPStatusCode'],
                        'http_headers': {
                            'date': buckets['ResponseMetadata']['HTTPHeaders']['date'],
                            'x-clv-request-id': buckets['ResponseMetadata']['HTTPHeaders']['x-clv-request-id'],
                            'x-clv-s3-version': buckets['ResponseMetadata']['HTTPHeaders']['x-clv-s3-version'],
                            'accept-ranges': buckets['ResponseMetadata']['HTTPHeaders']['accept-ranges'],
                            'x-amz-request-id': buckets['ResponseMetadata']['HTTPHeaders']['x-amz-request-id'],
                            'content-type': buckets['ResponseMetadata']['HTTPHeaders']['content-type'],
                            'content-length': buckets['ResponseMetadata']['HTTPHeaders']['content-length'],
                        },
                        'retry_attempts': buckets['ResponseMetadata']['RetryAttempts']
                    },
                    'Buckets': {
                        'name': bucket_dict['bucket-a']['Name'],
                        'creation_date': bucket_dict['bucket-a']['CreationDate']
                    },
                    'Owner':
                        {'display_name': buckets['Owner']['DisplayName'],
                         'id': buckets['Owner']['ID']
                         }
                }
                bucket_name = bucket_dict['bucket-a']['Name']

                ##################################
                # 2. Make Base Data
                ##################################
                bucket_data = ArchiveBucketGroup(buckets, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                bucket_resource = ArchiveStorageResource({
                    'name': bucket_name,
                    'data': bucket_data,
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                resource_responses.append(ArchiveStorageResponse({'resource': bucket_resource}))

                ##################################
                # 5. Make Resource Response Object
                ##################################
                resource_responses.append(ArchiveStorageResponse({'resource': bucket_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] bucket_group_name => {bucket_group.Buckets.Name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ObjectStorage', 'Bucket', bucket_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses
