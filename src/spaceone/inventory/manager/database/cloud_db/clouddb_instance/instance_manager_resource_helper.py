import logging

from spaceone.inventory.connector import CloudDBConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.database.clouddb.data import CloudDBConfig, CloudDBConfigGroup, AccessControlGroup, CloudDBServerInstance, CloudDBInstance

_LOGGER = logging.getLogger(__name__)


class InstanceManagerResourceHelper(NaverCloudManager):
    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: CloudDBConnector = ncloud_connector

    def get_cloud_db_info(self, instance, zone_info):

        cloud_db_dic = {}
        config_data = self._get_config(instance)
        config_group_data = self._get_config_group(instance)
        access_control_group_data = self._get_access_control_group(instance)
        cloud_db_server_data = self._get_cloud_db_server_data(instance)

        cloud_db_dic.update({
            'data': {
                'cloud_db_serviceName': instance.cloud_db_service_name,
                'db_kindCode': instance.db_kind_code,
                'engineVersion': instance.engine_version,
                'cpuCount': instance.cpu_count,
                'memorySize': instance.memory_size,
                'dataStorageType': instance.data_storage_type.code,
                'licenseCode': instance.license_code,
                'cloud_db_port': instance.cloud_db_port,
                'isHa': instance.is_ha,
                'backupTime': instance.backup_time,
                'backupFileRetentionPeriod': instance.backup_file_retention_period,
                'cloud_db_instanceStatusName': instance.cloud_db_instance_status_name,
                'collation': instance.collation,
                'createDate': instance.create_date,
                'zone': zone_info.get('zone', ''),
                'region_code': zone_info.get('region', ''),
                'cloud_db_config': config_data,
                'cloud_db_configGroup': config_group_data,
                'access_control_group': access_control_group_data,
                'cloud_db_serverInstance': cloud_db_server_data,
            }
        })

        return cloud_db_dic

    # @staticmethod
    # def _get_cloud_db_dic(instance, zone_info):
    #     cloud_db_data = {
    #         'name': instance.server_name,
    #         'instance_type': instance.server_instance_type,
    #         'provider': 'naver_cloud',
    #         'region_code': zone_info.get('region', '')
    #     }
    #
    #     return cloud_db_data

    @staticmethod
    def _get_cloud_db_server_data(instance):

        cloud_db_server_data = {
            'cloud_db_serverInstanceStatusName': instance.cloud_db_server_instance_status_name,
            'cloud_db_serverName': instance.cloud_db_server_name,
            'cloud_db_serverRole': instance.cloud_db_server_role.code,
            'cloud_db_serverPrivateDnsNAme': instance.private_dns_name,
            'cloud_db_serverPublicDnsName': instance.public_dns_name,
            'cloud_db_dataStorageSize': instance.data_storage_size,
            'cloud_db_usedDataStorageSize': instance.used_data_storage_size,
            'cloud_db_createDate': instance.create_date,
            'cloud_db_uptime': instance.uptime,

        }

        return CloudDBServerInstance(cloud_db_server_data, strict=False)

    @staticmethod
    def _get_config(instance):
        config_data = {
            'configName': instance.config_name,
            'configValue': instance.config_value
        }

        return CloudDBConfig(config_data, strict=False)

    @staticmethod
    def _get_config_group(instance):

        config_group_data = {
            'configGroupType': instance.config_group_type,
            'configGroupName': instance.config_group_name,
        }

        return CloudDBConfigGroup(config_group_data, strict=False)

    @staticmethod
    def _get_access_control_group(instance):

        access_control_group_data = {
            'access_control_groupName': instance.access_control_group_name,
            'access_control_groupDescription': instance.access_control_group_description,
            'createDate': instance.create_date,
        }

        return AccessControlGroup(access_control_group_data, strict=False)
