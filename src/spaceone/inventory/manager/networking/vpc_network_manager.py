import time
import logging
from typing import Tuple, List

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.connector.networking.vpc_connector import NetworkingConnector
from spaceone.inventory.model.networking.vpc_network.data import VPC
from spaceone.inventory.model.networking.vpc_network.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.networking.vpc_network.cloud_service import VPCNetworkResponse, VPCNetworkResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)

class VPCNetworkManager(NaverCloudManager):
    connector_name = 'NetworkingConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    vpc_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[VPCNetworkResponse], List[ErrorResourceResponse]]:
        _LOGGER.debug(f'** VPC Network START **')
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

        self.vpc_conn: NetworkingConnector = self.locator.get_connector(self.connector_name, **params)
        self.vpc_conn.set_connect(params['secret_data'])

        vpc_list = self.vpc_conn.list_vpc()


        # access_control_group_list = self._get_access_control_group(instance.access_control_group_list)
        # cloud_server_list = self._get_cloud_db_server_info(instance.cloud_db_server_instance_list)

        for vpc in vpc_list:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################

                network_vpc_name = vpc.vpc_name
                subnet_list = self._get_subnet_list(vpc.subnet_list)
                # vpc_peering_list = self.(vpc.vpc_peering_list)
                # round_table_list = self._get_subnet_list(vpc.round_table_list)
                # nat_gateway_instance_list = self._get_subnet_list(vpc.nat_gateway_instance_list)
                # network_acl_list = self._get_subnet_list(vpc.network_acl_list)


                vpc_info = {
                        'vpc_no': vpc.vpc_no,
                        'vpc_name': vpc.vpc_name,
                        'ipv4_cidr_block': vpc.ipv4_cidr_block,
                        'vpc_status': vpc.vpc_status.code,
                        'region_code': vpc.region_code,
                        'create_date': vpc.create_date,
                        'subnet_list': subnet_list,
                        # 'vpc_peering_list':  vpc_peering_list,
                        # 'round_table_list': round_table_list,
                        # 'nat_gateway_instance_list': nat_gateway_instance_list,
                        # 'network_acl_list': network_acl_list

                    # 'productCodeList': product_list,
                    # 'configGroupList': config_group_info
                }

                ##################################
                # 2. Make Base Data
                ##################################
                vpc_data = VPC(vpc_info, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                vpc_network_resource = VPCNetworkResource({
                    'name': network_vpc_name,
                    'data': vpc_data
                })

                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(VPCNetworkResponse({'resource': vpc_network_resource}))

            except Exception as e:
                _LOGGER.error(f'[list_resources] vm_id => {vpc.vpc_name}, error => {e}',exc_info=True)
                error_response = self.generate_resource_error_response(e, 'networking', 'vpc', network_vpc_name)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses

    # def get_list_resources(self) -> dict:
    #
    #     return {
    #         'vpc': self.vpc_conn.list_vpc(),
    #         'subnet': self.vpc_conn.list_Subnet(),
    #     }

    @staticmethod
    def _get_subnet_list(subnets):
        # Convert database list(dict) -> list(database object)
        subnet_list = []
        for subnet in subnets:
            subnet_data = {
                'subnet_no': subnet.subnet_no,
                'vpc_no': subnet.vpc_no,
                'zone_code': subnet.zone_code,
                'subnet_name': subnet.subnet_name,
                'subnet_status': subnet.subnet_status.code,
                'create_date': subnet.create_date,
                'subnet_type': subnet.subnet_type.code,
                'usage_type': subnet.usage_type.code,
                'network_acl_no': subnet.network_acl_no,


            }
            subnet_list.append(subnet_data)

        return subnet_list

    # @staticmethod
    # def _get_vpc_peering_list(peerings):
    #     # Convert database list(dict) -> list(database object)
    #     peering_list = []
    #     for peering in peerings:
    #         subnet_data = {
    #             'vpc_peering_instance_no': peering.vpc_peering_instance_no,
    #             'vpc_peering_name': peering.vpc_peering_name,
    #             'last_modifiy_date': peering.last_modifiy_date,
    #             'vpc_peering_instance_status_name': peering.vpc_peering_instance_status_name,
    #             'vpc_peering_instance_operation': peering.vpc_peering_instance_operation,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #             'vpc_peering_instance_status': peering.vpc_peering_instance_status,
    #
    #         }
    #         peering_list.append(subnet_data)
    #
    #     return peering_list