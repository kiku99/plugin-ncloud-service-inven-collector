import time
import logging
from typing import Tuple, List

from datetime import datetime, timedelta
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector
from spaceone.inventory.model.storage.object_storage.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.object_storage.cloud_service import ObjectStorageResource, ObjectStorageResponse
from spaceone.inventory.model.storage.object_storage.data import BucketGroup
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class ObjectStorageManager(NaverCloudManager):
    connector_name = 'ObjectStorageConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[ObjectStorageResponse], List[ErrorResourceResponse]]:
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
        self.instance_conn: ObjectStorageConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.object_storage_connect(params['secret_data'])

        buckets = self.instance_conn.list_buckets()
        objects = self.instance_conn.list_objects(params['bucket_name'])
        bucket_cors = self.instance_conn.get_bucket_cors(params['bucket_name'])

        list_buckets = buckets['Buckets']
        for bucket in list_buckets:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                bucket_name = bucket['Name']
                bucket = {
                    'buckets': {
                        'name': bucket['Name'],
                        'creation_date':  bucket['CreationDate']
                    },
                    'owner': {
                        'display_name': buckets['Owner']['DisplayName'],
                        'id': buckets['Owner']['ID']
                    }
                }
                ##################################
                # 2. Make Base Data
                ##################################
                bucket_data = BucketGroup(bucket, strict=False)
                date_info = bucket_data.buckets.creation_date
                ##################################
                # 3. Make Return Resource
                ##################################
                bucket_resource = ObjectStorageResource({
                    'name': bucket_name,
                    'data': bucket_data,
                    'launched_at': date_info
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(ObjectStorageResponse({'resource': bucket_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] bucket_group_name => {bucket_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ObjectStorage', 'Bucket', bucket_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

