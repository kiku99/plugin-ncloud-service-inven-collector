from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_clouddb
from ncloud_clouddb.rest import ApiException

__all__ = ['CloudDBConnector']


class CloudDBConnector(NaverCloudConnector):
    service = 'clouddb'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_cloud_db_instance(self):

        instance_list = []
        get_cloud_db_instance_list_request = ncloud_clouddb.GetCloudDBInstanceListRequest()

        try:
            api_response = self.clouddb_client.get_cloud_db_instance_list(get_cloud_db_instance_list_request)
            # print(api_response)
            for instance in api_response.cloud_db_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return instance_list

    def list_backup(self):
        backup_list = []

        get_backup_list_request = ncloud_clouddb.GetBackupListRequest()

        try:
            api_response = self.clouddb_client.get_block_storage_instance_list(get_backup_list_request)
            for instance in api_response.backup_file_list:
                backup_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return backup_list

    def list_object_storage_backup(self):
        object_storage_backup_list = []
        get_object_storage_backup_list_request = ncloud_clouddb.GetObjectStorageBackupListRequest()

        try:
            api_response = self.client.get_object_storage_backup_list(get_object_storage_backup_list_request)
            for instance in api_response.dms_file_list:
                object_storage_backup_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return object_storage_backup_list
