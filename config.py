import codecs
import json
import os
import subprocess
import sys
from functools import cache, lru_cache
from typing import Dict, List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = codecs.encode(os.urandom(32), "hex").decode()
    DB_PATH: str = "sqlite:///data.sqlite"

    class Config:
        env_file = ".env"

    def __getitem__(self, item: str):
        return getattr(self, item)


def get_secret_key() -> str:
    return get_config("SECRET_KEY")


@lru_cache()
def get_config(item: Optional[str] = None):
    if item:
        return Settings()[item]
    return Settings()
