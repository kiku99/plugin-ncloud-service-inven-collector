import time
import logging
from typing import Tuple, List

from spaceone.inventory.connector.management.monitoring_connector import MonitoringConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.management.monitoring.data import Metric, MetricStatistic
from spaceone.inventory.model.management.monitoring.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.model.management.monitoring.cloud_service import MonitoringResponse, MonitoringResource
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class MonitoringManager(NaverCloudManager):
    connector_name = 'MonitoringConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES
    instance_conn = None

    def collect_cloud_service(self, params) -> Tuple[List[MonitoringResponse], List[MonitoringResource]]:
        _LOGGER.debug(f'** Monitoring START **')
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
        self.instance_conn: MonitoringConnector = self.locator.get_connector(self.connector_name, **params)
        self.instance_conn.set_connect(params['secret_data'])

        metric_list = self.instance_conn.list_metrics(params["options"]["instance_no"])

        #metirc_statistic_list = self.instance_conn.list_metric_statistic(params["instance_no"], params["metric_name"], params["period"], params["start_time"], params["end_time"])

        for metric in metric_list:
            try:
                ##################################
                # 1. Set Basic Information
                ##################################
                instance_no = metric.instance_no
                metric_info = {
                    #'instance_no': metric.instance_no,
                    'metric_name': metric.metric_name,

                }
                ##################################
                # 2. Make Base Data
                ##################################
                metric_data = Metric(metric_info, strict=False)



                ##################################
                # 3. Make Return Resource
                ##################################
                monitoring_resource = MonitoringResource({
                    'name': instance_no,
                    # 'launched_at': autoscaling_group_create_date,
                    'data': metric_data
                })
                ##################################
                # 4. Make Resource Response Object
                ##################################
                resource_responses.append(MonitoringResponse({'resource': monitoring_resource}))

            except Exception as e:
                _LOGGER.error(
                    f'[list_resources] instance_no => {metric.instance_no}, error => {e}',
                    exc_info=True)
                error_response = self.generate_resource_error_response(e, 'Management', 'Monitoring', instance_no)
                error_responses.append(error_response)

        _LOGGER.debug(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return resource_responses, error_responses


    @staticmethod
    def _get_metric(metrics):
        # Convert database list(dict) -> list(database object)
        metric_list = []
        for metric in metrics:
            metric_data = {
                'metric_name': metric.metric_name,
                'instance_no': metric.instance_no
            }
            metric_list.append(metric_data)

        return metric_list

    @staticmethod
    def _get_DataPoint(metrics):
        # Convert database list(dict) -> list(database object)
        data_point_list = []
        for metric in metrics:
            data_point_data = {
                'timestamp': metric.timestamp,
                'average': metric.average,
                'unit': metric.unit,
            }
            data_point_list.append(data_point_data)

        return data_point_list



