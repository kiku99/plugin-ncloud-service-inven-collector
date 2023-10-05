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
        instance = self.autoscaling_connector.List_Adjustment_Type()
        print(instance)

    def test_list_Autoscaling_Activity_Log(self):
        instance = self.autoscaling_connector.List_Autoscaling_Activity_Log()
        print(instance)

    def test_list_Autoscaling_Configuration_Log(self):
        instance = self.autoscaling_connector.List_Autoscaling_Configuration_Log()
        print(instance)

    def test_list_Autoscaling_Group(self):
        instance = self.autoscaling_connector.List_Autoscaling_Group()
        print(instance)

    def test_list_Autoscaling_Policy(self):
        instance = self.autoscaling_connector.List_Autoscaling_Policy()
        print(instance)

    def test_list_Launch_Configuration(self):
        instance = self.autoscaling_connector.List_Launch_Configuration()
        print(instance)

    def test_list_Scaling_Process_Type_List(self):
        instance = self.autoscaling_connector.List_Scaling_Process_Type()
        print(instance)

    def test_list_Scheduled_Action_List(self):
        instance = self.autoscaling_connector.List_Scheduled_Action()
        print(instance)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
