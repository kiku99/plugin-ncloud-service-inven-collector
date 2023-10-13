CONNECTORS = {
    'NaverCloudConnector': {
            'backend': 'spaceone.inventory.libs.connector.NaverCloudConnector',
        },
    'ServerConnector': {
        'backend': 'spaceone.inventory.connector.compute.ServerConnector'
    },
    'AutoscalingConnector': {
        'backend': 'spaceone.inventory.connector.compute.AutoscalingConnector'
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
