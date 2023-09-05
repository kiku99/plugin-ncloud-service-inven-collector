import logging

from spaceone.inventory.connector import ServerConnector
from spaceone.inventory.libs.manager import NaverCloudManager

_LOGGER = logging.getLogger(__name__)


class NaverCloudManagerResourceHelper(NaverCloudManager):
    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: ServerConnector = ncloud_connector


    def get_naver_cloud_info(self, instance):
        return naver_cloud