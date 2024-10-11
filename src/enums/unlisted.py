from enum import Enum, IntEnum, IntFlag


class ImgUrls(IntEnum):
    # input for many requests
    NO_URLS = 0
    CDN = 1
    OPF = 2


class AuthType(IntEnum):
    # 19.39
    NONE = 1  # doc says 0
    USER = 2  # doc says 1


class DeviceCategoryFlags(IntEnum):
    # 19.40
    DO_NOT_COUNT = 1


class DeviceStatus(IntEnum):
    # 19.41
    DISABLED = 0
    ENABLED = 1


class HouseholdProductStatus(IntEnum):
    # 19.65
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


class DeviceActivityType(IntEnum):
    # 17.1 19.104
    RECORD = 1
    DELETE_REC = 2
    PPV_PURCHASE = 3
    TVOD_PURCHASE = 4
    EST_PURCHASE = 5
    PLAY_NPVR = 6
    PLAY_FVOD = 7
    PLAY_SVOD = 8
    PLAY_CUTV = 9
    PLAY_TVOD = 10
    PLAY_EST = 11
    PLAY_STOP = 12
    PURCHASE_PROD = 13
    RATE_ASSET = 14
    PLAY_LIVE = 15
    CUSTOM = 16
    PLAY_PLTV = 17
    PLAY_RETV = 18
    LOGIN = 19
    LOGOUT = 20
    DEVICE_ACTIVATION = 21


#    UNKNOWN_22 = 22
#    UNKNOWN_23 = 23
#    UNKNOWN_24 = 24
#    UNKNOWN_25 = 25


class HouseholdStatus(IntEnum):
    # 19.52
    DISABLED = 0
    ENABLED = 1
    DELETING = 2
    SUSPENDED = 3


class LoginSessionType(IntEnum):
    # 19.109
    ACCESS = 1
    REFRESH = 2
    GUEST = 3


class LoginStatus(str, Enum):
    # 1.1
    IN_SESSION = "IN_SESSION"
    LOGIN_OK = "LOGIN_OK"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    BAD_USERNAME_OR_PASSWORD = "BAD_USERNAME_OR_PASSWORD"
    MUST_CHANGE_PASSWORD = "MUST_CHANGE_PASSWORD"
    UNKNOWN = "UNKNOWN"


class LogoutStatus(str, Enum):
    # 2.1
    OK = "OK"
    BAD_SESSION = "BAD_SESSION"
    NO_SESSION = "NO_SESSION"


class ChangePasswordResult(IntEnum):
    # 9.5 9.6
    OK = 0
    INVALID_OLD_PASSWORD = 1


class DomainStatus(IntEnum):
    # 19.31
    DISABLED = 0
    ENABLED = 1


class DomainFlags(IntFlag):
    # 19.31
    RESTRICTED_DOMAIN = 1
    INHERIT_PRODUCTS_FILTER = 2
    INHERIT_SERVICES_FILTER = 4
    INHERIT_BLOCKOUTS = 8
    INHERIT_SERVICES_LIST = 16
    INHERIT_SERVICES_FUTURE_FILTER = 32
    GUEST_MODE = 64


class LoginResultStatus(str, Enum):
    # 19.48
    LOGIN_OK = "LOGIN_OK"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    BAD_USERNAME_OR_PASSWORD = "BAD_USERNAME_OR_PASSWORD"
    MUST_CHANGE_PASSWORD = "MUST_CHANGE_PASSWORD"


class ProductCategory(IntEnum):
    # 19.56
    FEATURE = 1
    GROUP = 2
    APPLICATION = 3
    PGI = 4


class ProductStatus(IntEnum):
    # 19.26 19.27 19.28 19.55 19.56 19.65 19.83
    DISABLED = 0
    ENABLED = 1


class UserSecurityType(IntEnum):
    # 19.45 19.61 9.44
    USER = 1
    GROUP = 2


class UserStatus(IntEnum):
    # 19.49
    DISABLED = 0
    ENABLED = 1
    LOCKED = 2
    MUST_CHG_PWD = 3


class ServiceType(IntEnum):
    # 19.22 19.119
    TV_CHANNEL = 1
    RADIO_CHANNEL = 2
    VOD_LIBRARY = 3


class QamValues(str, Enum):
    # Used in Domain Custom Data
    QAM16 = "16-QAM"
    QAM32 = "32-QAM"
    QAM64 = "64-QAM"
    QAM128 = "128-QAM"
    QAM256 = "256-QAM"


class ServiceStatus(IntEnum):
    # 19.22
    DISABLED = 0
    ENABLED = 1
    DELETING = 2


class KeywordType(str, Enum):
    MAIN = "main"
    SECONDARY = "secondary"
    OTHER = "other"


class LanguageISO639_2(str, Enum):
    ENGLISH = "eng"
    RUSSIAN = "rus"


class LanguageISO639_1(str, Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"


class AudioType(str, Enum):
    ORIGINAL = "original"
    DUBBED = "dubbed"


class BundleDisplayType(str, Enum):
    MIXED = 'mixed_bundle'
    FEATURE = 'feature_bundle'
    CHANNEL = 'channel_bundle'
    ON_DEMAND = 'on_demand_bundle'

#from Service Custom Data
class PpvWatchFree(str, Enum):
    ANY = 'ANY'
    PPV_SUBSCR = 'PPV_SUBSCR'
    NONE = 'NONE'


#from messaging (found in Nexx4.0 Hosted env operations manual)
class ClientNotificationScreens(str, Enum):
    ALL = 'ALL'
    ALL_EXCEPT_PLAYER = 'ALL_EXCEPT_PLAYER'
    PLAYER = 'PLAYER'
    HOME = 'HOME'
    ON_DEMAND = 'ON_DEMAND'
    MY_LIBRARY = 'MY_LIBRARY'


class AttachmentType(IntEnum):
    VIDEO = 1
    IMAGE = 2