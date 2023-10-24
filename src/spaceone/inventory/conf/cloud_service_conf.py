MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region',
                           'inventory.ErrorResource']
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
FILTER_FORMAT = []

CLOUD_SERVICE_GROUP_MAP = {
    'ComputeServer': [
        'ServerInstanceManager',
        'AutoscalingManager'
    ],
    'Database': [
      'CloudDBManager'
    ],
    'Storage': [
        'ObjectStorageManager',
        'ArchiveStorageManager'
    ],
    'Management': [
        'MonitoringManager'
    ],

    'Networking': [
        'VPCNetworkManager'
    ],
    'Content Delivery': [
        'CdnManager'
    ]
}

# not use
ASSET_URL = 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/naver_cloud'

REGION_INFO = {
    "KR": {"name": "Korea"}
}