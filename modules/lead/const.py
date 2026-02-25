from enum import Enum


class ModuleConfig(str, Enum):
    MODULE_NAME = "lead"
    MODULE_VERSION = "1.0.0"
    COLLECTION_NAME = "leads"


COLLECTION_NAME = ModuleConfig.COLLECTION_NAME.value
