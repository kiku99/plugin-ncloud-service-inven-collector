import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import Product
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

        cloud_db_img_products_llist = self.instance_conn.list_img_product(params["dbKindCode"])
        cloud_db_config_groups = self.instance_conn.list_config_group(params["dbKindCode"])
        cloud_db_products = self.instance_conn.list_product(params['cloudDBImageProductCode'])
        config_group_info = self._get_config_group(cloud_db_config_groups)

        for product in cloud_db_products:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                cloud_db_productCode = product.product_code
                matched_product_code_list = self._get_matched_product_code_list(cloud_db_img_products_llist, cloud_db_productCode)

                product_group = {
                    # 'autoscalingGroup': {
                    #     'defaultCooldown': autoscaling_group.default_cooldown,
                    #     'desiredCapacity': autoscaling_group.desired_capacity,
                    #     'healthCheckGracePeriod': autoscaling_group.health_check_grace_period,
                    #     'healthCheckType': autoscaling_group.health_check_type.code,
                    #     # 'inAutoScalingGroupServerInstanceList': autoscaling_group.in_auto_scaling_group_server_instance_list,
                    #     # 'loadBalancerInstanceSummaryList': autoscaling_group.load_balancer_instance_summary_list,
                    #     'maxSize': autoscaling_group.max_size,
                    #     'minSize': autoscaling_group.min_size
                    # },
                    'productCodeList': matched_product_code_list,
                    #'configGroupList':config_group_info
                }

                ##################################
                # 2. Make Base Data
                ##################################
                cloud_db_data = Product(product_group, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                cloud_db_resource = CloudDBResource({
                    'name': cloud_db_productCode,
                    # 'launched_at': autoscaling_group_create_date,
                    'data': cloud_db_data
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(CloudDBResponse({'resource': cloud_db_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] cloud_db_productCode => {product.product_code}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'database', 'CloudDB', cloud_db_productCode)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    @staticmethod
    def _get_matched_product_code_list(product_code_list, product):
        product_code_list_info = []

        for productCode in product_code_list:
            if productCode == product:
                product_data = {
                    'addStorageSize': productCode.add_block_stroage_size,
                    'baseStorageSize': productCode.base_block_storage_size,
                    'dbKindCode': productCode.db_kind_code,
                    'cpuCount': productCode.cpu_count,
                    'infraType': productCode.infra_resource_type.code,
                    'memorySize': productCode.memory_size,
                    'osInfo': productCode.os_information,
                    'platformType': productCode.platform_type.code,
                    'productCode': productCode.product_code,
                    'productDescription': productCode.product_description,
                    'productName': productCode.product_name,
                    'productType': productCode.product_type.code,
                }
                product_code_list_info.append(product_data)

        return product_code_list_info



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




    #     cloud_db_instances = self.instance_conn.list_cloud_db_instance()
    #
    #     for cloud_db in cloud_db_instances:
    #         try:
    #             ##################################
    #             # 1. Set Basic Information
    #             ##################################
    #             cloud_db_no = cloud_db.cloud_db_instance_no
    #             zone, region = self._get_zone_and_region(cloud_db)
    #             zone_info = {'zone': zone, 'region': region}
    #
    #
    #             cloud_db = {
    #                 'cloud_dbData' : {
    #                     'cloud_db_serviceName': cloud_db.cloud_db_service_name,
    #                     'db_kindCode': cloud_db.db_kind_code,
    #                     'engineVersion': cloud_db.engine_version,
    #                     'cpuCount': cloud_db.cpu_count,
    #                     'memorySize': cloud_db.memory_size,
    #                     'dataStorageType': cloud_db.data_storage_type.code,
    #                     'licenseCode': cloud_db.license_code,
    #                     'cloud_db_port': cloud_db.cloud_db_port,
    #                     'isHa': cloud_db.is_ha,
    #                     'backupTime': cloud_db.backup_time,
    #                     'backupFileRetentionPeriod': cloud_db.backup_file_retention_period,
    #                     'cloud_db_cloud_dbStatusName': cloud_db.cloud_db_cloud_db_status_name,
    #                     'collation': cloud_db.collation,
    #                     'createDate': cloud_db.create_date,
    #                     'zone': zone_info.get('zone', ''),
    #                     'region_code': zone_info.get('region', ''),
    #                     'cloud_db_config': config_data,
    #                     'cloud_db_configGroup': config_group_data,
    #                     'access_control_group': access_control_group_data,
    #                     'cloud_db_servercloud_db': cloud_db_server_data,
    #         }
    #             }
    #
    #             ##################################
    #             # 2. Make Base Data
    #             ##################################
    #             resource = self.get_cloud_db_instance_resource(zone_info, cloud_db, all_resources)
    #
    #             ##################################
    #             # 3. Make Collected Region Code
    #             ##################################
    #             self.set_region_code(resource.get('region', ''))
    #
    #             ##################################
    #             # 4. Make Resource Response Object
    #             ##################################
    #             resource_responses.append(CloudDBInstanceResponse({'resource': resource}))
    #
    #         except Exception as e:
    #             _LOGGER.error(f'[list_resources] vm_id => {cloud_db.server_instance_no}, error => {e}',
    #                           exc_info=True)
    #             error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Server', cloud_db_no)
    #             error_responses.append(error_response)
    #
    #     _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
    #     return resource_responses, error_responses
    #
    #
    # @staticmethod
    # def _get_zone_and_region(instance) -> (str, str):
    #     zone_name = instance.zone.zone_name
    #     region_name = instance.region.region_name
    #     return zone_name, region_name
    #
    # @staticmethod
    # def _get_backup_list(backups, cloud_db):
    #     backup_list_info = []
    #
    #     for backup in backups:
    #         if cloud_db == backup.cloud_db_instance_no:
    #             backup_info = {
    #                 'hostName': backup.host_name,
    #                 'fileName': backup.file_name,
    #                 'databaseName': backup.database_name,
    #                 'firstLSN': backup.first_lsn,
    #                 'lastLSN': backup.last_lsn,
    #                 'backupType': backup.backup_type.code,
    #                 'backupStartTime': backup.backup_start_time,
    #                 'backupEndTime': backup.backup_end_time
    #             }
    #             backup_list_info.append(backup_info)
    #
    #     return backup_list_info
    #
    #
    # @staticmethod
    # def _get_object_storage_backup_list(storage_list, cloud_db):
    #     storage_list_info = []
    #     for storage in storage_list:
    #         if cloud_db == storage_list.cloud_db_instance_no and cloud_db == storage_list.folder_name:
    #             object_storage_backup_data = {
    #                 'fileLength': storage.file_length,
    #                 'last_writeTime': storage.last_write_time,
    #                 'fileName': storage.file_name,
    #             }
    #             storage_list_info.append(object_storage_backup_data)
    #
    #     return storage_list_info
    #
    # @staticmethod
    # def _get_product_list(products, cloud_db):
    #     storage_list_info = []
    #     for product in products:
    #         if cloud_db == product.cloudDBInstanceNo and cloud_db == storage_list.folderName:
    #             object_storage_backup_data = {
    #                 'fileLength': storage.file_length,
    #                 'last_writeTime': storage.last_write_time,
    #                 'fileName': storage.file_name,
    #             }
    #             storage_list_info.append(object_storage_backup_data)
    #
    #     return storage_list_info