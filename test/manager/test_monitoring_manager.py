import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.management.monitoring_connector import MonitoringConnector
from spaceone.inventory.manager.management.monitoring.monitoring_manager import MonitoringManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestMonitoringeManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'

        cls.monitoring_connector = MonitoringConnector(secret_data=cls.secret_data)
        cls.monitoring_manager = MonitoringManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_server_instance_manager(self):
        secret_data = self.secret_data

        params = {'option': {}, 'secret_data': secret_data, 'filter': {}, 'instance_no': '19845517',
                'instanceNoList': ['19845517'],
                'metric_name': 'DiskWriteBytes',
                'period': 1800,
                'start_time': '2022-10-01T00:00:00Z',
                'end_time': '2023-10-13T23:59:59Z'}

        monitoring = self.monitoring_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(monitoring[0][0].to_primitive())

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
