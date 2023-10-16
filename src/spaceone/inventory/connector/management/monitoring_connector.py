from spaceone.inventory.libs.connector import NaverCloudConnector
import ncloud_monitoring
from ncloud_clouddb.rest import ApiException

__all__ = ['MonitoringConnector']


class MonitoringConnector(NaverCloudConnector):
    service = 'monitoring'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_metrics(self, instance_no):

        metrics_list = []
        get_metrics_list_request = ncloud_monitoring.GetListMetricsRequest(instance_no=instance_no)

        try:
            api_response = self.monitoring_client.get_list_metrics(get_metrics_list_request)
            # print(api_response)
            for instance in api_response.metrics:
                metrics_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_list_metrics: %s\n" % e)

        return metrics_list

    def list_metric_statistic(self, instanceNoList, metricName, period, startTime, endTime):
        metric_statistic_list = []

        get_metric_statistic_list_request = ncloud_monitoring.GetMetricStatisticListRequest(instance_no_list=instanceNoList, metric_name=metricName, period=period, start_time=startTime, end_time=endTime)

        try:
            api_response = self.monitoring_client.get_metric_statistic_list(get_metric_statistic_list_request)
            for instance in api_response.metric_statistic_list:
                metric_statistic_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_backup_list: %s\n" % e)

        return metric_statistic_list

