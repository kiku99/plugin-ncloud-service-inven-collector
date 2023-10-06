import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.instance_manager_resource_helper import \
    InstanceManagerResourceHelper
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.backup_manager_resource_helper import \
    BackUpManagerResourceHelper
from spaceone.inventory.manager.database.cloud_db.clouddb_instance.object_storage_manager_resource_helper import \
    ObjectStorageBackupManagerResourceHelper
from spaceone.inventory.model.database.clouddb.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.database.clouddb.cloud_service import CloudDBInstanceResponse, CloudDBResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)

class CloudDBeManager(NaverCloudManager):
    connector_name = 'CloudDBConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[CloudDBInstanceResponse], List[ErrorResourceResponse]]:
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
        all_resources = self.get_all_resources()
        cloud_db_instances = self.instance_conn.list_cloud_db_instance()

        for cloud_db in cloud_db_instances:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                cloud_db_no = cloud_db.cloud_db_instance_no
                zone, region = self._get_zone_and_region(cloud_db)
                zone_info = {'zone': zone, 'region': region}

                ##################################
                # 2. Make Base Data
                ##################################
                resource = self.get_cloud_db_instance_resource(zone_info, cloud_db, all_resources)

                ##################################
                # 3. Make Collected Region Code
                ##################################
                self.set_region_code(resource.get('region', ''))

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(CloudDBInstanceResponse({'resource': resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {cloud_db.server_instance_no}, error => {e}',
                              exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeServer', 'Server', cloud_db_no)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    def get_all_resources(self) -> dict:

        return {
            'object_storage_backup': self.instance_conn.list_object_storage_backup(),
            'backup': self.instance_conn.list_backup(),
        }

    def get_cloud_db_instance_resource(self, zone_info, instance, all_resources) -> CloudDBResource:
        """ Prepare input params for call manager """

        ################## TBD ######################

        # VPC
        # vpcs = all_resources.get('vpcs', [])
        subnets = all_resources.get('subnets', [])

        # All Public Images
        public_images = all_resources.get('public_images', {})

        # URL Maps
        url_maps = all_resources.get('url_maps', [])
        backend_svcs = all_resources.get('backend_svcs', [])
        target_pools = all_resources.get('target_pools', [])

        # Forwarding Rules
        forwarding_rules = all_resources.get('forwarding_rules', [])

        # Firewall
        firewalls = all_resources.get('firewalls', [])

        # Get Instance Groups
        instance_group = all_resources.get('instance_group', [])

        # Get Machine Types
        instance_types = all_resources.get('instance_type', [])

        # Autoscaling group list
        autoscaler = all_resources.get('autoscaler', [])

        # storages
        storage_backups = all_resources.get('object_storage_backup', [])

        # login keys
        backups = all_resources.get('backup', [])

        '''Get related resources from managers'''
        cloud_db_instance_manager_helper: InstanceManagerResourceHelper = \
            InstanceManagerResourceHelper(self.instance_conn)
        object_storage_backup_manager_helper: ObjectStorageBackupManagerResourceHelper = \
            ObjectStorageBackupManagerResourceHelper()
        backup_manager_helper: BackUpManagerResourceHelper = BackUpManagerResourceHelper()

        object_storage_backup = object_storage_backup_manager_helper.get_object_storage_backup_info(storage_backups)
        backup = backup_manager_helper.get_backup_info(backups)
        cloud_db_data = cloud_db_instance_manager_helper.get_cloud_db_info(instance, zone_info)

        ''' Gather all resources information '''

        cloud_db_data['data'].update({
            'loginKey': backup,
            'storage': object_storage_backup,
        })

        cloud_db_data.update({

            'instance_type': cloud_db_data.get('data', {}).get('compute', {}).get('serverInstanceType', {}),
            'instance_size': cloud_db_data.get('data', {}).get('hardware', {}).get('cpuCount', 0),
            'launched_at': cloud_db_data.get('data', {}).get('compute', {}).get('createDate', '')
        })
        return CloudDBResource(cloud_db_data, strict=False)

    @staticmethod
    def _get_zone_and_region(instance) -> (str, str):
        zone_name = instance.zone.zone_name
        region_name = instance.region.region_name
        return zone_name, region_name
