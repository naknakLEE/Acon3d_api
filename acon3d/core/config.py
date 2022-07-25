from functools import lru_cache
from typing import Dict, Type

from core.base import AppEnvTypes, BaseAppSettings
from core.app import AppSettings
from core.development import DevAppSettings



@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = DevAppSettings
    return config()