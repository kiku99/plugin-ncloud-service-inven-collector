import json
import os
import unittest

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)

if AKI is None or SK is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your NCloud credential first for test

        ##################################################
        example)

        export NAVER_APPLICATION_CREDENTIALS="<PATH>" 
    """)
    exit


# def _get_credentials():
#     with open(NAVER_APPLICATION_CREDENTIALS_PATH) as json_file:
#         json_data = json.load(json_file)
#         return json_data


class TestCollector(TestCase):

    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK
    }

    def test_init(self):
        print(self.secret_data)
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        print(self.secret_data)
        options = {}
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': self.secret_data})
        print_json(v_info)

    def test_collect(self):
        print(self.secret_data)
        '''
        Options can be selected
        options = {"cloud_service_types": ["SQLWorkspace"]}
                        "service_code_mappers": {
                    "Compute Engine": "Test Gikang",
                    "Networking": "HaHa HoHo",
                    "Cloud SQL": "SQLSQL"
            }
        '''
        options = {
            # "cloud_service_types": ["CloudFunctions"],
            # "cloud_service_types": ["Compute"]
            # "custom_asset_url": 'http://xxxxx.spaceone.dev/icon/google'
        }
        filter = {}

        resource_stream = self.inventory.Collector.collect({
            'options': options,
            'secret_data': self.secret_data,
            'filter': filter})

        print(resource_stream)
        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
