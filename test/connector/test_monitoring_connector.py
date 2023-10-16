import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.management.monitoring_connector import MonitoringConnector
AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestMonitoringConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.monitoring_connector = MonitoringConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_metrics(self):
        metrics = self.monitoring_connector.list_metrics(instance_no='19845517')

        print(metrics)

    def test_list_metric_statistic(self):
        metric_statistic = self.monitoring_connector.list_metric_statistic(instanceNoList=['19845517'], metricName='DiskWriteBytes', period=1800, startTime='2022-10-01T00:00:00Z', endTime='2023-10-13T23:59:59Z')

        print(metric_statistic)




if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
