from spaceone.inventory.libs.connector import NaverCloudConnector
# import swiftclient
# from keystoneauth1 import session
# from keystoneauth1.identity import v3
# import pprint

__all__ = ['ArchiveStorageConnector']

container_name = 'sample-container'

class ArchiveStorageConnector(NaverCloudConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_buckets(self):
        container = self.archive_storage_client.get_account()
        return container

    def list_objects(self, container_name):
        container = self.archive_storage_client.get_container(container_name)
        return container

    # ({'content-type': 'application/json; charset=utf-8', 'x-account-container-count': '3',
    #   'x-account-object-count': '12', 'x-account-bytes-used': '85390701', 'x-timestamp': '1697636873.41315',
    #   'x-account-storage-policy-standard00-container-count': '3',
    #   'x-account-storage-policy-standard00-object-count': '12',
    #   'x-account-storage-policy-standard00-bytes-used': '85390701', 'accept-ranges': 'bytes', 'content-length': '305',
    #   'x-account-project-domain-id': 'default', 'x-trans-id': 'tx053a45e3a03f4566864d2-00653400ac',
    #   'x-openstack-request-id': 'tx053a45e3a03f4566864d2-00653400ac', 'date': 'Sat, 21 Oct 2023 16:47:40 GMT'},
    #  [{'name': 'bucket-A', 'count': 1, 'bytes': 93, 'last_modified': '2023-10-18T13:47:53.427630'},
    #   {'name': 'sample-container', 'count': 2, 'bytes': 43, 'last_modified': '2023-10-18T14:01:10.912160'},
    #   {'name': 'segment-container', 'count': 9, 'bytes': 85390565, 'last_modified': '2023-10-18T14:38:27.759670'}])




