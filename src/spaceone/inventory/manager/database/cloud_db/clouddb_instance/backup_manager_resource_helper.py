import logging

from spaceone.inventory.connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import BackupFile

_LOGGER = logging.getLogger(__name__)


class BackUpManagerResourceHelper(NaverCloudManager):
    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: CloudDBConnector = ncloud_connector

    def get_backup_info(self, backups):

        for backup in backups:

            backup_info = {
                'hostName': backup.host_name,
                'fileName': backup.file_name,
                'databaseName': backup.database_name,
                'firstLSN': backup.first_lsn,
                'lastLSN': backup.last_lsn,
                'backupType': backup.backup_type.code,
                'backupStartTime': backup.backup_start_time,
                'backupEndTime': backup.backup_end_time
            }

        return BackupFile(backup_info, strict=False)
