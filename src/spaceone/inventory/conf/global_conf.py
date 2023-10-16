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

    'CloudDBConnector': {
        'backend': 'spaceone.inventory.connector.database.CloudDBConnector'
    },
    'ManagementConnector': {
        'backend': 'spaceone.inventory.connector.management.ManagementConnector'
    },
    'CdnConnector': {
        'backend': 'spaceone.inventory.connector.content_delivery.CdnConnector'
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
