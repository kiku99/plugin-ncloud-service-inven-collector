from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.server.data import Storage


class StorageManagerResourceHelper(NaverCloudManager):
    connector_name = 'ServerConnector'

    def get_storage_info(self, instance, storage_list):
        """
        storage_data = {'block_storage_instance_description': "",
            'block_storage_instance_no': '',
            'block_storage_instance_operation': {'code': 'NULL',
                                                    'code_name': 'Block Storage NULLOP'},
            'block_storage_instance_status': {'code': 'ATTAC',
                                                'code_name': 'Block storage ATTACHED state'},
            'block_storage_instance_status_name': 'attached',
            'block_storage_name': '',
            'block_storage_product_code': '',
            'block_storage_size': ,
            'block_storage_type': {'code': 'BASIC', 'code_name': 'Basic BS'},
            'create_date': '',
            'device_name': '/dev/xvda',
            'disk_detail_type': {'code': 'HDD', 'code_name': 'HDD'},
            'disk_type': {'code': 'NET', 'code_name': 'Network Storage'},
            'max_iops_throughput': None,
            'member_server_image_no': None,
            'region': {'region_code': 'KR', 'region_name': 'Korea', 'region_no': '1'},
            'server_instance_no': '',
            'server_name': '',
            'zone': {'region_no': '1',
                        'zone_code': 'KR-2',
                        'zone_description': '평촌 zone',
                        'zone_name': 'KR-2',
                        'zone_no': '3'}}
        """

        storage_sz = float(instance.base_block_storage_size)
        matching_single_storage = self._get_matched_storage_tag_info(instance, storage_list)
        if matching_single_storage is not None:
            single_storage_type, single_storage_detail_type = self._get_storage_type(matching_single_storage)

        single_disk = {
            'storageName': matching_single_storage.block_storage_name,
            'storageSize': storage_sz,
            'storageDescription': matching_single_storage.block_storage_instance_description,
            'storageDiskType': single_storage_type,
            'storageDiskDetailType': single_storage_detail_type
        }

        # storages.append(Storage(single_disk, strict=False))
        return Storage(single_disk, strict=False)

    @staticmethod
    def _get_matched_storage_tag_info(instance, storage_list):
        source_storage = None
        source = instance.server_instance_no
        storage = [storage_single for storage_single in storage_list if storage_single.server_instance_no == source]
        if len(storage) > 0:
            source_storage = storage[0]
        return source_storage

    @staticmethod
    def _get_storage_type(matching_single_storage_tag):
        type = matching_single_storage_tag.block_storage_type.code_name
        type_detail = matching_single_storage_tag.disk_detail_type.code_name
        return type, type_detail

