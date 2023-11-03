import logging

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.server.data import Compute, Hardware, PortForwardingRules, IP
from spaceone.inventory.connector.compute.server_connector import ServerConnector

_LOGGER = logging.getLogger(__name__)


class ServerInstanceManagerResourceHelper(NaverCloudManager):
    connector_name = 'ServerConnector'
    instance_conn = None

    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: ServerConnector = ncloud_connector

    def get_server_info(self, instance, zone_info):
        server_dic = self._get_server_dic(instance, zone_info)
        hardware_data = self._get_hardware_data(instance)
        compute_data = self._get_compute_data(instance, zone_info)
        port_forwarding_rules = self._get_port_forwarding_rules(instance)
        ip_info = self._get_ip(instance)

        server_dic.update({
            'data': {
                'compute': compute_data,
                'port_forwarding_rules': port_forwarding_rules,
                'hardware': hardware_data,
                'ip': ip_info
            }
        })
        return server_dic

    @staticmethod
    def _get_server_dic(instance, zone_info):
        server_data = {
            'name': instance.server_name,
            'instance_type': instance.server_instance_type,
            'provider': 'naver_cloud',
            'region_code': zone_info.get('region', '')
        }

        return server_data

    @staticmethod
    def _get_hardware_data(instance):
        """
        cpu_count = IntType(default=0)
        memory_size = LongType(default=0.0)
        """

        cpu_count = instance.cpu_count
        memory_size = instance.memory_size

        hardware_data = {
            'cpu_count': cpu_count,
            'memory_size': memory_size,
        }

        return Hardware(hardware_data, strict=False)

    @staticmethod
    def _get_compute_data(instance, zone_info):
        compute_data = {
            'server_instance_no': instance.server_instance_no,
            'server_name': instance.server_name,
            'server_image_name': instance.server_image_name,
            'server_instance_status': instance.server_instance_status.code,
            'server_instance_operation': instance.server_instance_operation.code,
            'server_instance_status_name': instance.server_instance_status_name,
            'platform_type': instance.platform_type.code_name,
            'create_date': instance.create_date,
            'uptime': instance.uptime,
            'server_image_product_code': instance.server_image_product_code,
            'server_product_code': instance.server_product_code,
            'server_instance_type': instance.server_instance_type.code,
            'zone': zone_info.get('zone', ''),
            'region': zone_info.get('region', '')
        }

        return Compute(compute_data, strict=False)

    @staticmethod
    def _get_port_forwarding_rules(instance):
        port_forwarding_rules_data = {
            'port_forwarding_external_port': instance.port_forwarding_external_port,
            'port_forwarding_internal_port': instance.port_forwarding_internal_port,
            'port_forwarding_public_ip': instance.port_forwarding_public_ip
        }

        return PortForwardingRules(port_forwarding_rules_data, strict=False)

    @staticmethod
    def _get_ip(instance):
        ip_data = {
            'private_ip': instance.private_ip,
            'public_ip': instance.public_ip
        }

        return IP(ip_data, strict=False)
