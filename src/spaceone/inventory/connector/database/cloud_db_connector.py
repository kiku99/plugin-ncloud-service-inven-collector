from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_clouddb
from ncloud_clouddb.rest import ApiException

__all__ = ['CloudDBConnector']


class CloudDBConnector(NaverCloudConnector):
    service = 'clouddb'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_cloud_db_instance(self, db_kind_code):

        instance_list = []
        get_cloud_db_instance_list_request = ncloud_clouddb.GetCloudDBInstanceListRequest(db_kind_code=db_kind_code)

        try:
            api_response = self.clouddb_client.get_cloud_db_instance_list(get_cloud_db_instance_list_request)
            # print(api_response)
            for instance in api_response.cloud_db_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cloud_db_instance_list: %s\n" % e)

        return instance_list

    def list_backup(self, cloudDBInstanceNo):
        backup_list = []

        get_backup_list_request = ncloud_clouddb.GetBackupListRequest(cloud_db_instance_no=cloudDBInstanceNo)

        try:
            api_response = self.clouddb_client.get_backup_list(get_backup_list_request)
            for instance in api_response.backup_file_list:
                backup_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_backup_list: %s\n" % e)

        return backup_list

    def list_object_storage_backup(self, cloudDBInstanceNo, folderName):
        object_storage_backup_list = []
        get_object_storage_backup_list_request = ncloud_clouddb.GetObjectStorageBackupListRequest(cloud_db_instance_no=cloudDBInstanceNo, folder_name=folderName)

        try:
            api_response = self.clouddb_client.get_object_storage_backup_list(get_object_storage_backup_list_request)

            for instance in api_response.dms_file_list:
                object_storage_backup_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_object_storage_backup_list: %s\n" % e)
        return object_storage_backup_list

    def list_product(self, cloudDBImageProductCode):
        product_list = []
        get_product_request = ncloud_clouddb.GetCloudDBProductListRequest(cloud_db_image_product_code=cloudDBImageProductCode)

        try:
            api_response = self.clouddb_client.get_cloud_db_product_list(get_product_request)

            for instance in api_response.product_list:
                product_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cloud_db_product_list: %s\n" % e)

        return product_list

    def list_img_product(self, dbKindCode):
        img_product_list = []
        get_img_product_request = ncloud_clouddb.GetCloudDBImageProductListRequest(db_kind_code=dbKindCode)

        try:
            api_response = self.clouddb_client.get_cloud_db_image_product_list(get_img_product_request)

            for instance in api_response.product_list:
                img_product_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cloud_db_image_product_list: %s\n" % e)

        return img_product_list

    def list_dms_operation(self, requestNo):
        operation_list = []
        get_operation_request = ncloud_clouddb.GetDmsOperationRequest(request_no=requestNo)

        try:
            api_response = self.clouddb_client.get_dms_operation(get_operation_request)

            for instance in api_response.cloud_db_instance_list:
                operation_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_dms_operation: %s\n" % e)

        return operation_list

    def list_config_group(self, dbKindCode):
        config_group_list = []
        get_config_group_request = ncloud_clouddb.GetCloudDBConfigGroupListRequest(db_kind_code=dbKindCode)

        try:
            api_response = self.clouddb_client.get_cloud_db_config_group_list(get_config_group_request)

            for instance in api_response.cloud_db_config_group_list:
                config_group_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cloud_db_config_group_list: %s\n" % e)

        return config_group_list
