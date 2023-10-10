import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import Product,Clouddbinstance
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.instance_manager_resource_helper import \
    InstanceManagerResourceHelper
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.backup_manager_resource_helper import \
    BackUpManagerResourceHelper
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.object_storage_manager_resource_helper import \
    ObjectStorageBackupManagerResourceHelper
from spaceone.inventory.model.database.clouddb.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.database.clouddb.cloud_service import CloudDBResponse, CloudDBResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class CloudDBManager(NaverCloudManager):
    connector_name = 'CloudDBConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[CloudDBResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** CloudDB START **')
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        resource_responses = []
        error_responses = []
        start_time = time.time()

        ##################################
        # 0. Gather All Related Resources
        ##################################
        self.instance_conn: CloudDBConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])

        cloud_db_img_products_list = self.instance_conn.list_img_product(params["dbKindCode"])
        cloud_db_config_groups = self.instance_conn.list_config_group(params["dbKindCode"])
        cloud_db_products = self.instance_conn.list_product(params['cloudDBImageProductCode'])
        config_group_info = self._get_config_group(cloud_db_config_groups)

        for product in cloud_db_products:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                cloud_db_productName = product.product_name
                #product_list = self._get_product_list(product)


                product = {
                    'productGroup':{
                        'baseStorageSize': product.base_block_storage_size,
                         #'dbKindCode': product.db_kind_code,
                         'cpuCount': product.cpu_count,
                         'infraType': product.infra_resource_type.code,
                         'memorySize': product.memory_size,
                         #'osInfo': product.os_information,
                         'platformType': product.platform_type,
                         'productCode': product.product_code,
                         'productDescription': product.product_description,
                         'productName': product.product_name,
                         'productType': product.product_type.code,
                    },

                    #'productCodeList': product_list,
                    #'configGroupList': config_group_info
                }


                ##################################
                # 2. Make Base Data
                ##################################
                cloud_db_data = Clouddbinstance(product, strict=False)



                ##################################
                # 3. Make Return Resource
                ##################################
                cloud_db_resource = CloudDBResource({
                    'name': cloud_db_productName,
                    # 'launched_at': autoscaling_group_create_date,
                    'data': cloud_db_data
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(CloudDBResponse({'resource': cloud_db_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] cloud_db_productName => {product.product_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'database', 'CloudDB', cloud_db_productName)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_config_group(config_groups):
        # Convert database list(dict) -> list(database object)
        config_group_list = []
        for group in config_groups:
            config_group_data = {
                'configGroupType': group.config_group_type,
                'configGroupName': group.config_group_name,
                'configGroupNo': group.config_group_no,
            }
            config_group_list.append(config_group_data)

        return config_group_list




