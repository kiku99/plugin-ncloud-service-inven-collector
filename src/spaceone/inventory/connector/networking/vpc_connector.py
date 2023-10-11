import ncloud_vpc

from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_server
from ncloud_server.rest import ApiException

__all__ = ['NetworkingConnector']


class NetworkingConnector(NaverCloudConnector):
    service = 'Network'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_vpc(self):
        vpc_list = []
        get_vpc_list_request = ncloud_vpc.GetVpcListRequest()

        try:
            api_response = self.vpc_client.get_vpc_list(get_vpc_list_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                vpc_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return vpc_list

    def vpc_Detail(self):
        vpc_detail = []
        get_vpc_detail_request = ncloud_vpc.GetVpcDetailRequest()

        try:
            api_response = self.vpc_client.get_vpc_detail(get_vpc_detail_request)
            for instance in api_response.block_storage_instance_list:
                vpc_detail.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return vpc_detail

    def list_Subnet(self):
        subnet_list = []
        get_subnet_list_request = ncloud_vpc.GetSubnetListRequest()

        try:
            api_response = self.vpc_client.get_subnet_list(get_subnet_list_request)
            for instance in api_response.block_storage_instance_list:
                subnet_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_block_storage_instance_list: %s\n" % e)

        return subnet_list

    #
    # def Subnet_Detail(self):
    #     subnet_detail = []
    #     get_subnet_detail_request = ncloud_vpc.GetSubnetDetailRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_subnet_detail(get_subnet_detail_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             subnet_detail.append(instance)
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return subnet_detail

    def Network_AclList(self):
        network_aclList = []
        get_Network_AclList_request = ncloud_vpc.GetNetworkAclListRequest()

        try:
            api_response = self.vpc_client.get_network_acl_list(get_Network_AclList_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                network_aclList.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return network_aclList

    def Network_AclDetail(self):
        network_aclDetail = []
        get_Network_AclDetail_request = ncloud_vpc.GetNetworkAclDetailRequest()

        try:
            api_response = self.vpc_client.get_Network_AclDetail(get_Network_AclDetail_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                network_aclDetail.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return network_aclDetail

    # def List_Network_Acl_Rule(self):
    #     Network_AclRule_List = []
    #     get_Network_AclRule_List_request = ncloud_vpc.GetNetworkAclRuleListRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_network_acl_rule_list(get_Network_AclRule_List_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             Network_AclRule_List.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return Network_AclRule_List

    def List_Nat_Gateway_Instance(self):
        Nat_Gateway_Instance_List = []
        get_Nat_Gateway_Instance_List_request = ncloud_vpc.GetNatGatewayInstanceListRequest()

        try:
            api_response = self.vpc_client.get_nat_gateway_instance_list(get_Nat_Gateway_Instance_List_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                Nat_Gateway_Instance_List.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return Nat_Gateway_Instance_List

    # def Nat_Gateway_Instance_Detail(self):
    #     nat_gateway_instance_detail = []
    #     get_Nat_Gateway_Instance_Detail_request = ncloud_vpc.GetNatGatewayInstanceDetailRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_Nat_Gateway_Instance_Detail(get_Nat_Gateway_Instance_Detail_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             nat_gateway_instance_detail.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return nat_gateway_instance_detail

    def List_Vpc_Peering_Instance(self):
        Vpc_Peering_Instance_List = []
        get_Vpc_Peering_Instance_List_request = ncloud_vpc.GetVpcPeeringInstanceListRequest()

        try:
            api_response = self.vpc_client.get_vpc_peering_instance_list(get_Vpc_Peering_Instance_List_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                Vpc_Peering_Instance_List.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return Vpc_Peering_Instance_List

    # def Vpc_Peering_Instance_Detail(self):
    #     vpc_peering_instance_detail = []
    #     get_Vpc_Peering_Instance_Detail_request = ncloud_vpc.GetVpcPeeringInstanceDetailResponse()
    #
    #     try:
    #         api_response = self.vpc_client.getsubnet_detail(get_Vpc_Peering_Instance_Detail_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             vpc_peering_instance_detail.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return vpc_peering_instance_detail

    def List_Route_Table(self):
        route_table_list = []
        get_Route_Table_List_request = ncloud_vpc.GetRouteTableListRequest()

        try:
            api_response = self.vpc_client.get_route_table_list(get_Route_Table_List_request)
            # print(api_response)
            for instance in api_response.vpc_list:
                route_table_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return route_table_list

    # def Route_Table_Detail(self):
    #     route_table_detail = []
    #     get_Route_table_detail_request = ncloud_vpc.GetRouteTableDetailRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_Route_table_detail(get_Route_table_detail_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             route_table_detail.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return route_table_detail


    # def List_Route(self):
    #     route_list = []
    #     get_Route_List_request = ncloud_vpc.GetRouteListRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_route_list(get_Route_List_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             route_list.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return route_list

    # def List_Route_Table_Subnet(self):
    #     route_table_subnet_list = []
    #     get_Route_Table_Subnet_List_request = ncloud_vpc.GetRouteTableSubnetListRequest()
    #
    #     try:
    #         api_response = self.vpc_client.get_route_table_subnet_list(get_Route_Table_Subnet_List_request)
    #         # print(api_response)
    #         for instance in api_response.vpc_list:
    #             route_table_subnet_list.append(instance)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)
    #
    #     return route_table_subnet_list