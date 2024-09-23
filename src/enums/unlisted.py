from enum import Enum, IntEnum, IntFlag


class ProductStatus(IntEnum):
    # 19.26 19.27 19.28 19.55 19.56 19.65 19.83
    DISABLED = 0
    ENABLED = 1


class ProductType(IntEnum):
    # 19.28 19.65 19.83? 19.107 and others
    PAUSE = 1
    CATCHUP = 2
    RESTART = 3
    NPVR = 4
    PPV_FEAT = 5
    EST_FEAT = 6
    SVOD_FEAT = 7
    FVOD_FEAT = 8
    TVOD_FEAT = 9
    CHANNEL_GROUP = 10
    APPLICATION = 11
    PPV = 12
    SVOD = 13
    FVOD = 14
    TVOD = 15
    EST_DTO = 16


class BundleDisplayType(str, Enum):
    MIXED = 'mixed_bundle'
    FEATURE = 'feature_bundle'
    CHANNEL = 'channel_bundle'
    ON_DEMAND = 'on_demand_bundle'


class HouseholdStatus(IntEnum):
    # 19.52
    DISABLED = 0
    ENABLED = 1
    DELETING = 2
    SUSPENDED = 3
