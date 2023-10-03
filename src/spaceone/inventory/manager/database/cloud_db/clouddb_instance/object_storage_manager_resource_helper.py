import logging

from spaceone.inventory.connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import DmsFile

_LOGGER = logging.getLogger(__name__)


class ObjectStorageBackupManagerResourceHelper(NaverCloudManager):
    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: CloudDBConnector = ncloud_connector

    def get_object_storage_backup_info(self, storage_list):

        for storage in storage_list:

            object_storage_backup_data = {
                'fileLength': storage.file_length,
                'last_writeTime': storage.last_write_time,
                'fileName': storage.file_name,
            }

        return DmsFile(object_storage_backup_data, strict=False)
