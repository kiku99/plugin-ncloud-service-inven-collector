import time
import logging
from typing import Tuple, List

from datetime import datetime, timedelta
from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.storage.object_storage_connector import ObjectStorageConnector
from spaceone.inventory.model.storage.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.storage.cloud_service import ObjectStorageResource, ObjectStorageResponse
from spaceone.inventory.model.storage.data import BucketInstance
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class ObjectStorageManager(BaseManager):
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
        ##################################s
        self.instance_conn: ObjectStorageConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(**params)

        buckets = self.instance_conn.list_buckets()
        objects = self.instance_conn.list_objects(**params)
        bucket_cors = self.instance_conn.get_bucket_cors(**params)

        for bucket_group in buckets:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                bucket_info = bucket_group.ResponseMetadata.Buckets
                bucket_name = bucket_group.ResponseMetadata.Buckets.Name

                bucket_group = {
                    #'Response_Metadata': bucket_group.ResponseMetadata,
                    'Request_Id': bucket_group.ResponseMetadata.RequestId,
                    'Host_Id': bucket_group.ResponseMetadata.HostId,
                    'HTTP_StatusCode': bucket_group.ResponseMetadata.HTTPStatusCode,
                    #'HTTP_Headers': bucket_group.ResponseMetadata.HTTPHeaders,
                    'Date': bucket_group.ResponseMetadata.HTTPHeaders.date,
                    'Bucket_name' : bucket_group.Buckets.Name,
                    'Bucket_CreationDate': bucket_group.CreationDate,
                    'Retry_Attempts': bucket_group.ResponseMetadata.RetryAttempts,
                    'Buckets_info': bucket_group.Buckets,
                    'Bucket_owner': bucket_group.Buckets.Owner,
                    'Display_Name': bucket_group.Buckets.Owner.DisplayName,
                    'ID_': bucket_group.Buckets.Owner.ID
                }


                ##################################
                # 2. Make Base Data
                ##################################
                bucket_data = BucketInstance(bucket_group, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                bucket_resource = ObjectStorageResource({
                    'name': bucket_name,
                    'data': bucket_data,
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                resource_responses.append(ObjectStorageResponse({'resource': bucket_resource}))

                ##################################
                # 5. Make Resource Response Object
                # List of LoadBalancingResponse Object
                ##################################
                resource_responses.append(ObjectStorageResponse({'resource': bucket_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] bucket_group_name => {bucket_group.Buckets.Name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ObjectStorage', 'Bucket', bucket_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses





