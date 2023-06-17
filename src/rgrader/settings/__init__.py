from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import List, Literal, NewType, Tuple
from pydantic import BaseSettings, PostgresDsn, SecretStr
import os
from pprint import pprint


class InitialSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = ".env/rgrader.initial.env"
        env_file_encoding = "utf-8"

    env = "dev"


initial_settings = InitialSettings()


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = (
            ".env/rgrader.initial.env",
            f".env/rgrader.{initial_settings.env}.env",
        )
        env_file_encoding = "utf-8"

   




    

    

    


settings = AppSettings()
