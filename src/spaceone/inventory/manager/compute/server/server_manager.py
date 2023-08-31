import time
import logging

from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.computing.ServerConnector import ServerConnector
from spaceone.inventory.model.compute.server.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.compute.server.cloud_service import server_instance, \
    ServerInstanceResponse, ServerInstanceResource
from spaceone.inventory.model.compute.server.data import InstanceTag, InstanceTagList, InstanceGroup


_LOGGER = logging.getLogger(__name__)


class ServerManager(NaverCloudManager):
    connector_name = 'ServerConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Server START **')
        start_time = time.time()
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
        collected_cloud_services = []
        error_responses = []
        instance_group_id = ""

        secret_data = params['secret_data']
        project_id = secret_data['project_id']
        ## Server connector
        instance_group_conn: ServerConnector = self.locator.get_connector(self.connector_name, **params)

        ##################################
        # 0. Gather All Related Resources
        # List all information through connector
        ##################################
        instance_servers = instance_group_conn.list_Server_Instance()           #groups
        server_region = instance_group_conn.list_server_region()                #group_manager
        server_image_product = instance_group_conn.list_Server_Image_Product()  #auto
        server_zone = instance_group_conn.list_Server_Zone()                    #template

        for instance_server in instance_servers:
            try:

                ##################################
                # 1. Set Basic Information
                ##################################
                instance_server_id = instance_server.get('serverInstanceNo') #id

                instance_server.update({
                    'project': secret_data['project_id']
                })

                scheduler = {'type': 'zoneCode'} if 'zoneCode' in instance_server else {'type': 'regionCode'}

                if match_server_region := \
                        self.match_server_region(server_region, instance_server.get('regionCode')):

                    instance_server_type = self._get_instance_server_type(match_server_region)
                    scheduler.update({'instance_server_type': instance_server_type})

                    # Managed 우짜라는거임?
                    match_server_region.update({
                        'statefulPolicy': {
                            'preservedState': {'disks': self._get_stateful_policy(match_server_region)}}
                    })

                    ##################################
                    # 2. Make Base Data
                    ##################################
                    instance_server.update({
                        'instance_server_type': instance_server_type,
                        'instance_server_region': InstanceGroupManagers(match_server_region, strict=False)
                    })

                    if match_server_image_product := self.match_server_image_product(server_image_product, match_server_region):
                        scheduler.update(
                            self._get_auto_policy_for_scheduler(match_server_image_product)
                        )

                        instance_server.update({
                            'server_image_product': AutoScaler(match_server_image_product, strict=False),
                            #고쳐야함
                            'autoscaling_display': self._get_server_image_product_display(
                                match_server_image_product.get('productCode', {}))
                        })

                    match_server_zone = \
                        self.match_server_zone(server_zone,
                                               match_server_region.get('zoneCode'))

                    if match_server_zone:
                        instance_server.update({'zone': InstanceTemplate(match_server_zone, strict=False)})

                else:
                    # Unmanaged
                    instance_server.update({'instance_server_type': 'UNMANAGED'})
                    scheduler.update({'instance_server_type': 'UNMANAGED'})

                location_type = self._check_instance_server_is_zonal(instance_server)
                location = self._get_location(instance_server)
                region = self.parse_region_from_zone(location) if location_type == 'zone' else location
                instances = instance_group_conn.list_instances(instance_server.get('name'), location, location_type)

                display_loc = {'region': location, 'zone': ''} if location_type == 'region' \
                    else {'region': self.parse_region_from_zone(location), 'zone': location}

                google_cloud_monitoring_filters = [{'key': 'resource.labels.instance_group_name',
                                                    'value': instance_server.get('name')}]

                instance_server.update({
                    'power_scheduler': scheduler,
                    'instances': self.get_instances(instances),
                    'instance_counts': len(instances),
                    'display_location': display_loc,
                    'google_cloud_monitoring': self.set_google_cloud_monitoring(project_id,
                                                                                "compute.googleapis.com/instance_group",
                                                                                instance_server.get('name'),
                                                                                google_cloud_monitoring_filters)
                })
                # No labels
                _name = instance_server.get('name', '')
                instance_group_data = InstanceGroup(instance_server, strict=False)

                ##################################
                # 3. Make Return Resource
                ##################################
                instance_group_resource = ServerInstanceResource({
                    'name': _name,
                    'account': project_id,
                    'region_code': region,
                    'data': instance_group_data,
                    'reference': ReferenceModel(instance_group_data.reference())
                })

                ##################################
                # 4. Make Collected Region Code
                ##################################
                self.set_region_code(region)

                ##################################
                # 5. Make Resource Response Object
                # List of LoadBalancingResponse Object
                ##################################
                collected_cloud_services.append(ServerInstanceResponse({'resource': instance_group_resource}))
            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'ComputeEngine', 'InstanceGroup', instance_group_id)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services, error_responses

    def _get_location(self, instance_group):
        if 'zone' in instance_group:
            url_zone = instance_group.get('zone')
            location = self.get_param_in_url(url_zone, 'zones')
        else:
            # zone or region key must be existed
            url_region = instance_group.get('region')
            location = self.get_param_in_url(url_region, 'regions')

        return location

    def get_instances(self, instances):
        _instances = []
        for instance in instances:
            url_instance = instance.get('instance', '')
            instance.update({'name': self.get_param_in_url(url_instance, 'instances')})
            _instances.append(instance)

        return _instances

    @staticmethod
    def _check_instance_server_is_zonal(instance_group):
        instance_group_type = 'zone' if 'zone' in instance_group else 'region'
        return instance_group_type

    @staticmethod   #수정해야함
    def match_server_zone(instance_templates, instance_template_self_link):
        for instance_template in instance_templates:
            if instance_template['selfLink'] == instance_template_self_link:
                return instance_template

        return None

    @staticmethod   #수정해야함
    def match_server_region(instance_group_managers, instance_group_name):
        for instance_group_manager in instance_group_managers:
            if instance_group_manager['instanceGroup'] == instance_group_name:
                return instance_group_manager

        return None

    @staticmethod
    def match_autoscaler(autoscalers, instance_group_manager):
        match_autoscaler_name = instance_group_manager.get('status', {}).get('autoscaler')

        if match_autoscaler_name:
            for autoscaler in autoscalers:
                if match_autoscaler_name == autoscaler['selfLink']:
                    return autoscaler

        return None

    @staticmethod
    def _get_stateful_policy(match_instance_group_manager):
        disks_vos = []
        stateful_policy = match_instance_group_manager.get('statefulPolicy')
        if stateful_policy:
            preserved_state = stateful_policy.get('preservedState')
            if preserved_state:
                for key, val in preserved_state.get('disks', {}).items():
                    disks_vos.append({'key': key, 'value': val})

        return disks_vos

    @staticmethod
    def _get_instance_group_type(instance_group_manager):
        if instance_group_manager.get('status', {}).get('stateful', {}).get('hasStatefulConfig'):
            return 'STATEFUL'
        else:
            return 'STATELESS'

    def _get_autoscaling_display(self, autoscaling_policy):
        display_string = f'{autoscaling_policy.get("mode")}: Target '

        policy_display_list = []

        if 'cpuUtilization' in autoscaling_policy:
            policy_display_list.append(
                f'CPU utilization {(autoscaling_policy.get("cpuUtilization", {}).get("utilizationTarget")) * 100}%')

        if 'loadBalancingUtilization' in autoscaling_policy:
            policy_display_list.append(
                f'LB capacity fraction {(autoscaling_policy.get("loadBalancingUtilization", {}).get("utilizationTarget")) * 100}%')

        for custom_metric in autoscaling_policy.get('customMetricUtilizations', []):
            policy_display_list.append(
                f'{custom_metric.get("metric", "")} {custom_metric.get("utilizationTarget", "")}{self._get_custom_metric_target_type(custom_metric.get("utilizationTargetType"))}')

        if policy_display_list:
            policy_join_str = ', '.join(policy_display_list)
            return f'{display_string}{policy_join_str}'
        else:
            return ''

    @staticmethod
    def _get_custom_metric_target_type(util_target_type):
        if util_target_type == 'GAUGE':
            return ''
        elif util_target_type == 'DELTA_PER_SECOND':
            return '/s'
        elif util_target_type == 'DELTA_PER_MINUTE':
            return '/m'
        else:
            return ''

    @staticmethod
    def _get_auto_policy_for_scheduler(matched_scheduler) -> dict:
        auto_policy = matched_scheduler.get('autoscalingPolicy', {})

        if auto_policy != {}:
            return {
                'recommend_size': matched_scheduler.get('recommendedSize', 1),
                'origin_min_size': auto_policy.get('minNumReplicas'),
                'origin_max_size': auto_policy.get('maxNumReplicas'),
                'mode': auto_policy.get('mode')
            }
        else:
            return {}
