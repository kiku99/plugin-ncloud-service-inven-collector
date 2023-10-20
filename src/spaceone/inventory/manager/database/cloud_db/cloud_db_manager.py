import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.database.cloud_db_connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import CloudDBInstance
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
        cloud_db_instances = self.instance_conn.list_cloud_db_instance(params["dbKindCode"])
        cloud_db_products = self.instance_conn.list_product(params['cloudDBImageProductCode'])

        for instance in cloud_db_instances:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                cloud_db_service_name = instance.cloud_db_service_name
                cloud_db_create_date = instance.create_date
                zone_list = self._get_zone_list(instance.zone)
                region_list = self._get_region_list(instance.region)
                access_control_group_list = self._get_access_control_group(instance.access_control_group_list)
                cloud_server_list = self._get_cloud_db_server_info(instance.cloud_db_server_instance_list)

                instance_data = {
                        'cloud_db_instance_no': instance.cloud_db_instance_no,
                        'db_kind_code': instance.db_kind_code,
                        'cpu_count': instance.cpu_count,
                        'data_storage_type': instance.data_storage_type.code,
                        'license_code': instance.license_code,
                        'is_ha': instance.is_ha,
                        'cloud_db_port': instance.cloud_db_port,
                        'backup_time': instance.backup_time,
                        'backup_file_retention_period': instance.backup_file_retention_period,
                        'cloud_db_instance_status_name': instance.cloud_db_instance_status_name,
                        'zone_list': zone_list,
                        'region_list': region_list,
                        'access_control_group_list': access_control_group_list,
                        'cloud_db_server_instance_list': cloud_server_list,

                }


                ##################################
                # 2. Make Base Data
                ##################################
                cloud_db_data = CloudDBInstance(instance_data, strict=False)



                ##################################
                # 3. Make Return Resource
                ##################################
                cloud_db_resource = CloudDBResource({
                    'name': cloud_db_service_name,
                    'launched_at': cloud_db_create_date,
                    'data': cloud_db_data
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(CloudDBResponse({'resource': cloud_db_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] cloud_db_service_name => {instance.cloud_db_service_name}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'database', 'CloudDB', cloud_db_service_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_access_control_group(groups):
        # Convert database list(dict) -> list(database object)
        access_control_group_list = []
        for group in groups:
            access_control_group_data = {
                'access_control_group_name': group.access_control_group_name,
                'access_control_group_configuration_no': group.access_control_group_configuration_no,
                'access_control_group_description': group.access_control_group_description,
                'create_date': group.create_date,
            }
            access_control_group_list.append(access_control_group_data)

        return access_control_group_list

    @staticmethod
    def _get_cloud_db_server_info(servers):
        # Convert database list(dict) -> list(database object)
        cloud_db_server_info_list = []
        for server in servers:
            server = {
                'cloud_db_server_instance_no': server.cloud_db_server_instance_no,
                'cloud_db_server_name': server.cloud_db_server_name,
                'cloud_db_server_instance_status_name': server.cloud_db_server_instance_status_name,
                'cloud_db_server_role': server.cloud_db_server_role.code,
                'private_dns_name': server.private_dns_name,
                'data_storage_size': server.data_storage_size,
                'used_data_storage_size': server.used_data_storage_size,
                'create_date': server.create_date,
                'uptime': server.uptime

            }
            cloud_db_server_info_list.append(server)

        return cloud_db_server_info_list

    @staticmethod
    def _get_zone_list(zone):
        zone_list_info = []


        zone_info = {
                'zone_description': zone.zone_description,
                'zone_name': zone.zone_name,
                'zone_no': zone.zone_no
            }
        zone_list_info.append(zone_info)

        return zone_list_info

    @staticmethod
    def _get_region_list(region):
        region_list_info = []


        region_info = {
                'region_no': region.region_no,
                'region_code': region.region_code,
                'region_name': region.region_name
            }
        region_list_info.append(region_info)

        return region_list_info


