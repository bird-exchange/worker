import os

from pydantic import BaseModel


class AppConfig(BaseModel):
    endpoint: str
    temp_file_storage: str


def load_from_env() -> AppConfig:
    endpoint = os.environ['ENDPOINT']
    temp_file_storage = os.environ['TEMP_FILE_STORAGE']
    return AppConfig(endpoint=endpoint, temp_file_storage=temp_file_storage)


config = load_from_env()
