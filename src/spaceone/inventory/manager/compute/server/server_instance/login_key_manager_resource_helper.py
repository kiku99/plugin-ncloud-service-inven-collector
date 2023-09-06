import logging

from spaceone.inventory.connector import ServerConnector
from spaceone.inventory.libs.manager import NaverCloudManager
from spaceone.inventory.model.compute.server.data import LoginKey

_LOGGER = logging.getLogger(__name__)


class LoginKeyManagerResourceHelper(NaverCloudManager):
    def __init__(self, ncloud_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.instance_conn: ServerConnector = ncloud_connector

    def get_login_key_info(self, login_keys):
        login_key_data = []

        for login_key in login_keys:

            login_key_info = {
                'fingerPrint': login_key.fingerprint,
                'keyName': login_key.key_name,
                'createDate': login_key.create_date
            }

        return LoginKey(login_key_info, strict=False)
