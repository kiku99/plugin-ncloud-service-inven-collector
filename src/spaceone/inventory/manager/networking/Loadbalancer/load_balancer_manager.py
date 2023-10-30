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
    loadbalancer_conn = None

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

        self.vpc_conn: LoadbalancerConnector = self.locator.get_connector(self.connector_name, **params)
        self.vpc_conn.set_connect(params['secret_data'])

        vpc_list = self.vpc_conn.list_vpc()
        Route_Table_List = self.vpc_conn.List_Route_Table()
        Sub_net_List = self.vpc_conn.list_Subnet()
        peering_vpc_List = self.vpc_conn.List_Vpc_Peering_Instance()
        nat_gate_way_instance_List = self.vpc_conn.List_Nat_Gateway_Instance()
        net_work_acl_List = self.vpc_conn.Network_AclList()

        for vpc in vpc_list:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################

                Loadbalancer_name = LoadBalancerInstance.load_balancer_name
                Loadbalancer_create_date = LoadBalancerInstance.create_date
                Loadbalancer_no = LoadBalancerInstance.load_balancer_instance_no
                matched_route_table_list = self._get_matched_route_table_list(Route_Table_List, Loadbalancer_no)
                matched_subnet_list = self._get_matched_subnet_list(Sub_net_List, Loadbalancer_no)
                matched_vpc_peering_list = self._get_vpc_peering_list(peering_vpc_List, Loadbalancer_no)
                matched_nat_gateway_instance_list = self._get_nat_gateway_instance_list(nat_gate_way_instance_List, Loadbalancer_no)
                matched_network_acl_list = self._get_network_acl_list(net_work_acl_List, Loadbalancer_no)

                Loadbalancer_info = {
                        '_no': vpc.vpc_no,
                        # 'vpc_name': vpc.vpc_name,
                        'ipv4_cidr_block': vpc.ipv4_cidr_block,
                        'vpc_status': vpc.vpc_status.code,
                        'region_code': vpc.region_code,
                        # 'create_date': vpc.create_date,
                        'subnet_list': matched_subnet_list,
                        'vpc_peering_list':  matched_vpc_peering_list,
                        'route_table_list': matched_route_table_list,
                        'nat_gateway_instance_list': matched_nat_gateway_instance_list,
                        'network_acl_list': matched_network_acl_list

                }

                ##################################
                # 2. Make Base Data
                ##################################
                Loadbalancer_data = LoadBalancerInstance(Loadbalancer_info, strict=False)

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
                _LOGGER.error(f'[list_resources] vm_id => {vpc.vpc_name}, error => {e}',exc_info=True)
                error_response = self.generate_resource_error_response(e, 'networking', 'vpc', Loadbalancer_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_matched_subnet_list(Sub_net_List, subnet_group):
        # Convert database list(dict) -> list(database object)
        subnet_list = []
        for subnet in Sub_net_List:
            if subnet_group == subnet.vpc_no :
                subnet = {
                    'subnet_no': subnet.subnet_no,
                    'zone_code': subnet.zone_code,
                    'subnet_name': subnet.subnet_name,
                    'subnet_status': subnet.subnet_status.code,
                    # 'create_date': subnet.create_date,
                    'subnet_type': subnet.subnet_type.code,
                    'usage_type': subnet.usage_type.code,
                    'network_acl_no': subnet.network_acl_no,


            }
            subnet_list.append(subnet)

        return subnet_list

    @staticmethod
    def _get_vpc_peering_list(peering_vpc_List, peering_group):
        # Convert database list(dict) -> list(database object)
        vpc_peering_list_info = []
        for peering in peering_vpc_List:
            if peering_group == peering.vpc_no:
                peering = {
                    'vpc_peering_instance_no': peering.vpc_peering_instance_no,
                    'vpc_peering_name': peering.vpc_peering_name,
                    'last_modifiy_date': peering.last_modifiy_date,
                    'vpc_peering_instance_status': peering.vpc_peering_instance_status.code,
                    'vpc_peering_instance_status_name': peering.vpc_peering_instance_status_name,
                    'vpc_peering_instance_operation': peering.vpc_peering_instance_operation.code,
                    'source_vpc_no': peering.source_vpc_no,
                    'source_vpc_name': peering.source_vpc_name,
                    'source_vpc_ipv4_cidr_block': peering.source_vpc_ipv4_cidr_block,
                    'source_vpc_login_id': peering.source_vpc_login_id,
                    'target_vpc_no': peering.target_vpc_no,
                    'target_vpc_name': peering.target_vpc_name,
                    'target_vpc_ipv4_cidr_block': peering.target_vpc_ipv4_cidr_block,
                    'target_vpc_login_id': peering.target_vpc_login_id,
                    'vpc_peering_description': peering.vpc_peering_description,
                    'has_reverse_vpc_peering': peering.has_reverse_vpc_peering,
                    'is_between_accounts': peering.is_between_accounts,
                    'reverse_vpc_peering_instance_no': peering.reverse_vpc_peering_instance_no,

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