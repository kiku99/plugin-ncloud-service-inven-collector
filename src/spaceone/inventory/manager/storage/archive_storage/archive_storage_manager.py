import time
import logging
from typing import Tuple, List

from datetime import datetime, timedelta
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.storage.archive_storage_connector import ArchiveStorageConnector
from spaceone.inventory.model.storage.archive_storage.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.archive_storage.cloud_service import ArchiveStorageResource, ArchiveStorageResponse
from spaceone.inventory.model.storage.archive_storage.data import ArchiveBucketGroup
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

        #################################
        # 0. Gather All Related Resources
        ##################################
        self.instance_conn: ArchiveStorageConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])

        buckets = self.instance_conn.list_buckets()
        objects = self.instance_conn.list_objects(params['options']['bucket_name'])

        list_buckets = buckets[1]
        for bucket in list_buckets:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################

                bucket_name = bucket['name']
                bucket = {
                    'name': bucket['name'],
                    'count': bucket['count'],
                    'bytes': bucket['bytes'],
                    'last_modified': bucket['last_modified']
                }
                ##################################
                # 2. Make Base Data
                ##################################
                bucket_data = ArchiveBucketGroup(bucket, strict=False)
                date_info = bucket['last_modified']

                ##################################
                # 3. Make Return Resource
                ##################################
                bucket_resource = ArchiveStorageResource({
                    'name': bucket_name,
                    'data': bucket_data,
                    'launched_at': date_info
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
                    f'[list_resources] bucket_group_name => {bucket_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ObjectStorage', 'Bucket', bucket_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses
