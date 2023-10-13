import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.inventory.connector.compute.autoscaling_connector import AutoscalingConnector

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)


class TestAutoscalingConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')
        cls.schema = 'naver_client_secret'
        cls.autoscaling_connector = AutoscalingConnector(secret_data=cls.secret_data)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_Adjustment_Type(self):
        instance = self.autoscaling_connector.list_adjustment_type()
        print(instance)

    def test_list_Autoscaling_Activity_Log(self):
        instance = self.autoscaling_connector.list_autoscaling_activity_log()
        print(instance)

    def test_list_Autoscaling_Configuration_Log(self):
        instance = self.autoscaling_connector.list_autoscaling_configuration_log()
        print(instance)

    def test_list_Autoscaling_Group(self):
        instance = self.autoscaling_connector.list_autoscaling_group()
        print(instance)

    def test_list_Autoscaling_Policy(self):
        instance = self.autoscaling_connector.list_autoscaling_policy()
        print(instance)

    def test_list_Launch_Configuration(self):
        instance = self.autoscaling_connector.list_launch_configuration()
        print(instance)

    def test_list_Scaling_Process_Type_List(self):
        instance = self.autoscaling_connector.list_scaling_process_type()
        print(instance)

    def test_list_Scheduled_Action_List(self):
        instance = self.autoscaling_connector.list_scheduled_action()
        print(instance)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
