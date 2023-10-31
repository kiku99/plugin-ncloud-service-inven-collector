import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.connector.networking.Loadbalancer_connector import LoadbalancerConnector
from spaceone.inventory.model.networking.loadbalancer.data import LoadBalancerInstance
from spaceone.inventory.model.networking.loadbalancer.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.networking.loadbalancer.cloud_service import LoadBalancingResource, LoadBalancingResponse
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)

class LoadbalancerManager(NaverCloudManager):
    connector_name = 'LoadbalancerConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    load_balancer_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[LoadBalancingResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** Loadbalancer START **')
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

        self.load_balancer_conn: LoadbalancerConnector = self.locator.get_connector(self.connector_name, **params)
        self.load_balancer_conn.set_connect(params['secret_data'])

        load_balanced_server_instance_list = self.load_balancer_conn.list_load_balanced_server_instance(params["loadBalancerInstanceNo"])
        # load_balancer_instance_list = self.load_balancer_conn.list_load_balancer_instance()
        # ssl_List = self.load_balancer_conn.list_load_balancer_ssl_certificate()
        # target_server_instance_List = self.load_balancer_conn.list_load_balancer_target_server_instance()

        for Loadbalance in load_balanced_server_instance_list:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################

                Loadbalancer_name = LoadBalancerInstance.load_balancer_name
                Loadbalancer_create_date = LoadBalancerInstance.create_date
                Loadbalancer_no = LoadBalancerInstance.load_balancer_instance_no
                zone_list = self._get_zone_list(Loadbalance.zone)
                region_list = self._get_region_list(Loadbalance.region)



                Load_balance_data = {
                        'load_balancer_instance_no': Loadbalance.load_balancer_instance_no,
                        'virtual_ip': Loadbalance.virtual_ip,
                        'load_balancer_name': Loadbalance.ipv4_cidr_block,
                        'load_balancer_algorithm_type': Loadbalance.vpc_status.code,
                        'load_balancer_description': Loadbalance.region_code,
                        'create_date': Loadbalance.create_date,
                        'domain_name': Loadbalance.domain_name,
                        'internet_line_type':  Loadbalance.internet_line_type.code,
                        'load_balancer_instance_status_name': Loadbalance.load_balancer_instance_status_name,
                        'load_balancer_instance_status': Loadbalance.load_balancer_instance_status.code,
                        'load_balancer_instance_operation': Loadbalance.load_balancer_instance_operation.code,
                        'network_usage_type': Loadbalance.network_usage_type.code,
                        'is_http_keep_alive': Loadbalance.is_http_keep_alive,
                        'connection_timeout': Loadbalance.connection_timeout,
                        'certificate_name': Loadbalance.certificate_name,
                        'load_balancer_rule_list': Loadbalance.load_balancer_rule_list,
                        'load_balanced_server_instance_list': Loadbalance.load_balanced_server_instance_list,
                        'zone_list': zone_list,
                        'Region_list': region_list,

                }

                ##################################
                # 2. Make Base Data
                ##################################
                Loadbalancer_data = LoadBalancerInstance(Load_balance_data, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                vpc_network_resource = LoadBalancingResource({
                    'name': Loadbalancer_name,
                    'launched_at': Loadbalancer_create_date,
                    'data': Loadbalancer_data
                })

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(LoadBalancingResponse({'resource': vpc_network_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {Loadbalance.Loadbalancer_name}, error => {e}',exc_info=True)
                error_response = self.generate_resource_error_response(e, 'networking', 'Loadbalancer', Loadbalancer_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_zone_list(zone_List, zone_group):
        # Convert database list(dict) -> list(database object)
        Zone_list = []
        for zone in zone_List:
            if zone_group == zone_List.load_balancer_instance_no:
                zone = {
                    'subnet_no': zone_List.subnet_no,
                    'zone_code': zone_List.zone_code,
                    'zone_description': zone_List.zone_description
            }
            Zone_list.append(zone)

        return Zone_list

    @staticmethod
    def _get_region_list(zone_List, zone_group):
        # Convert database list(dict) -> list(database object)
        Zone_list = []
        for zone in zone_List:
            if zone_group == zone_List.load_balancer_instance_no :
                zone = {
                    'region_no': zone_List.subnet_no,
                    'region_code': zone_List.zone_code,
                    'region_name': zone_List.zone_description
            }
            Zone_list.append(zone)

        return Zone_list

    @staticmethod
    def _get_vpc_peering_list(peering_vpc_List, peering_group):
        # Convert database list(dict) -> list(database object)
        vpc_peering_list_info = []
        for peering in peering_vpc_List:
            if peering_group == peering.vpc_no:
                peering = {
                'zone_no' : peering.zone_no

                }
            vpc_peering_list_info.append(peering)

        return vpc_peering_list_info

    @staticmethod
    def _get_nat_gateway_instance_list(nat_gate_way_List, network_vpc_group):
        # Convert database list(dict) -> list(database object)
        nat_gateway_instance_list_info = []
        for gateway in nat_gate_way_List:
            if network_vpc_group == gateway.vpc_no:
                gateway = {
                    'nat_gateway_instance_no': gateway.nat_gateway_instance_no,
                    'nat_gateway_name': gateway.nat_gateway_name,
                    'public_ip': gateway.public_ip,
                    'nat_gateway_instance_status': gateway.nat_gateway_instance_status.code,
                    'nat_gateway_instance_status_name': gateway.nat_gateway_instance_status_name,
                    'nat_gateway_instance_operation': gateway.nat_gateway_instance_operation.code,
                    'nat_gateway_description' : gateway.nat_gateway_description

            }
            nat_gateway_instance_list_info.append(gateway)

        return nat_gateway_instance_list_info

    @staticmethod
    def _get_network_acl_list(net_work_acl_List, network_vpc_group):
        # Convert database list(dict) -> list(database object)
        network_acl_list_info = []
        for network_acl in net_work_acl_List:
            if network_vpc_group == network_acl.vpc_no:
                network_acl = {
                    'network_acl_no': network_acl.network_acl_no,
                    'nat_gateway_name': network_acl.network_acl_name,
                    'network_acl_status': network_acl.network_acl_status.code,
                    'network_acl_description': network_acl.network_acl_description,
                    'is_default': network_acl.is_default,
            }
            network_acl_list_info.append(network_acl)

        return network_acl_list_info

    @staticmethod
    def _get_matched_route_table_list(Route_Table_List, network_vpc_group):
        # Convert database list(dict) -> list(database object)
        route_table_list_info = []
        for route_table in Route_Table_List:
            if network_vpc_group == route_table.vpc_no:
                route_table = {
                    'route_table_name': route_table.route_table_name,
                    'route_table_no': route_table.route_table_no,
                    'is_default': route_table.is_default,
                    'supported_subnet_type': route_table.supported_subnet_type.code,
                    'route_table_status': route_table.route_table_status.code,
                    'route_table_description': route_table.route_table_description,

            }
            route_table_list_info.append(route_table)

        return route_table_list_info