import os

from pydantic import BaseModel


class AppConfig(BaseModel):
    endpoint: str
    temp_file_storage: str


class HandlerConfig(BaseModel):
    path_to_data: str
    path_load_model: str
    path_test_results: str
    image_size: int
    load_epoch: int
    switch: bool


def load_from_env() -> AppConfig:
    endpoint = os.environ['ENDPOINT']
    temp_file_storage = os.environ['TEMP_FILE_STORAGE']
    return AppConfig(endpoint=endpoint, temp_file_storage=temp_file_storage)


config = load_from_env()

handler_config = HandlerConfig(
    path_to_data='{}/testA/'.format(os.environ['TEMP_FILE_STORAGE']),
    path_load_model="worker/handler/checkpoints",
    path_test_results='{}/res/'.format(os.environ['TEMP_FILE_STORAGE']),
    image_size=256,
    load_epoch=300,
    switch=True
)
