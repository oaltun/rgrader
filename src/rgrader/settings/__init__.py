from datetime import datetime
from pathlib import Path
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

    excel_file_path: Path = Path("/mnt/c/Users/oguz/OneDrive/donem-2022-2/hesaplama_kurami/BLM2502 - 1_Final_Detay_Raporu_14-06-23-13-22.xlsx")
    excel_out_dir: Path = Path("/mnt/c/Users/oguz/OneDrive/donem-2022-2/hesaplama_kurami")

    # "A regular language is not a CFL ...", "Which one "matches to strings with even number ..."
    bad_questions:List[int] =[ 246160, 246036 ]

    max_possible_raw_points: float = float(380) - float(40)

    exam_start_time = datetime(year=2023,month=6,day=6,hour=9)
    exam_end_time = datetime(year=2023,month=6,day=6,hour=10,minute=10)


settings = AppSettings()
