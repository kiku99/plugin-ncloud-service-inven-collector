CONNECTORS = {
    'NaverCloudConnector': {
            'backend': 'spaceone.inventory.libs.connector.NaverCloudConnector',
        },
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ]
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}
