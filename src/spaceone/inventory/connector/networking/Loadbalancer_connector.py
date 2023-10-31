import ncloud_loadbalancer

from spaceone.inventory.libs.connector import NaverCloudConnector
from ncloud_server.rest import ApiException

__all__ = ['LoadbalancerConnector']


class LoadbalancerConnector(NaverCloudConnector):
    service = 'Network'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_load_balanced_server_instance(self, loadBalancerInstanceNo):
        load_balanced_server_instance_list = []
        get_server_instance = ncloud_loadbalancer.GetLoadBalancedServerInstanceListRequest(load_balancer_instance_no=loadBalancerInstanceNo)

        try:
            api_response = self.loadbalancer_client.get_load_balanced_server_instance_list(get_server_instance)
            for instance in api_response.server_instance_list:
                load_balanced_server_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_load_balanced_server_instance_list: %s\n" % e)

        return load_balanced_server_instance_list


    def list_load_balancer_instance(self):
        load_balancer_instance_list = []
        get_instance = ncloud_loadbalancer.GetLoadBalancerInstanceListRequest()

        try:
            api_response = self.loadbalancer_client.get_load_balancer_instance_list(get_instance)
            for instance in api_response.load_balancer_instance_list:
                load_balancer_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return load_balancer_instance_list


    def list_load_balancer_ssl_certificate(self):
        ssl_certificate_list = []
        get_ssl_certificate = ncloud_loadbalancer.GetLoadBalancerSslCertificateListRequest()

        try:
            api_response = self.loadbalancer_client.get_load_balancer_ssl_certificate_list(get_ssl_certificate)
            for instance in api_response.ssl_certificate_list:
                ssl_certificate_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return ssl_certificate_list


    def list_load_balancer_target_server_instance(self):
        target_server_instance_list = []
        get_target_server_instance = ncloud_loadbalancer.GetLoadBalancerTargetServerInstanceListRequest()

        try:
            api_response = self.loadbalancer_client.get_load_balancer_target_server_instance_list(get_target_server_instance)
            for instance in api_response.server_instance_list:
                target_server_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return target_server_instance_list