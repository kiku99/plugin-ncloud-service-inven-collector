import unittest
import os
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector import AutoscalingConnector
from spaceone.inventory.manager import AutoscalingManager

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestAutoscalingManager(TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'

        cls.autoscaling_connector = AutoscalingConnector(secret_data=cls.secret_data)
        cls.autoscaling_manager = AutoscalingManager()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_autoscaling_manager(self):
        secret_data = self.secret_data
        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        autoscaling_instances = self.autoscaling_manager.collect_cloud_service(params)
        # for server_instance in server_instances:
        #     print(server_instance.to_primitive())
        print(autoscaling_instances[0][0].to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
