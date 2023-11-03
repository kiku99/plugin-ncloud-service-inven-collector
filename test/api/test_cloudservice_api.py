import json
import os
import unittest

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)
# DI = os.environ.get("DOMAIN_ID", None)
# PI = os.environ.get('PROJECT_ID', None)

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
        'ncloud_secret_key': SK,
        'domain_id': 'default',
        'project_id': '25cd875760ea45fdbe6e0198a3e212cc',
        'db_kind_code': 'MYSQL',
        'cdn_instance_no': '20151001',
        'instance_no': '20150943',
        'bucket_name': 'buckettest0712'
    }

    def test_init(self):
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        # print(self.secret_data)
        options = {}
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': self.secret_data})
        print_json(v_info)

    def test_collect(self):
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
            "cloud_service_types": ["Compute"]
            # "custom_asset_url": 'http://xxxxx.spaceone.dev/icon/google'
        }
        filter = {}


        resource_stream = self.inventory.Collector.collect({
            'options': options,
            'secret_data': self.secret_data,
            'filter': filter})
            #'dbKindCode': dbKindCode, 'cdnInstanceNo': cdnInstanceNo, 'instance_no': instance_no})

        #print(resource_stream)
        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
