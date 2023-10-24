from spaceone.inventory.libs.connector import NaverCloudConnector

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




