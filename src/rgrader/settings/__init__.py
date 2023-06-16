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

    excel_file_path: Path = Path(
        "/mnt/c/Users/oguz/OneDrive/donem-2022-2/grafik/excel_final/BLM5234 - 1_Final_Detay_Raporu_16-06-23-14-25.xlsx"
    )
    excel_out_dir: Path = Path("/mnt/c/Users/oguz/OneDrive/donem-2022-2/grafik/excel_final")

    # List of bad question Ids. These will not contribute to final points.
    # eg. [ 246160, 246036 ]
    bad_questions: List[int] = []

    max_possible_raw_points: float = float(270)

    exam_start_time = datetime(year=2023, month=6, day=5, hour=19)
    exam_end_time = datetime(year=2023, month=6, day=5, hour=19, minute=40)

    puan_factor = 1.20
    zaman_factor = 0.20


settings = AppSettings()
