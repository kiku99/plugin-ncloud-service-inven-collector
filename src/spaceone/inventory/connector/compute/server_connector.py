from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_server
from ncloud_server.rest import ApiException

__all__ = ['ServerConnector']


class ServerConnector(NaverCloudConnector):
    service = 'compute'

    ##all add

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_server_region(self, **query):
        region_list = []
        query.update({'project': self.project_id})
        get_region_list_request = ncloud_server.GetRegionListRequest()

        try:
            api_response = self.client.get_server_instance_list(get_region_list_request)
            for region in api_response.regionList:
                region_list.append(region['regionCode'])
        except ApiException as e:
            print("Exception when calling V2Api->add_region_list: %s\n" % e)

        return region_list

    def list_Server_Image_Product(self, **query):
        server_image_product_list = []
        query.update({'project': self.project_id})
        get_server_image_product_list_request = ncloud_server.GetServerImageProductListRequest()

        try:
            api_response = self.client.get_server_image_product_list(get_server_image_product_list_request)
            for product in api_response.imageProductList:
                server_image_product_list.append(product['productCode'])
        except ApiException as e:
            print("Exception when calling V2Api->add_server_image_product_list: %s\n" % e)

        return server_image_product_list

    def list_Server_Zone(self, **query):

        zone_list = []
        query.update({'project': self.project_id})
        get_zone_list_request = ncloud_server.GetZoneListRequest()

        try:
            api_response = self.client.get_zone_list(get_zone_list_request)
            for zone in api_response.zoneList:
                zone_list.append(zone['zoneCode'])
        except ApiException as e:
            print("Exception when calling V2Api->get_zone_list: %s\n" % e)

        return zone_list

    def list_Server_Instance(self):

        instance_list = []
        get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()

        try:
            api_response = self.client.get_server_instance_list(get_server_instance_list_request)
            # print(api_response)
            for instance in api_response.server_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return instance_list