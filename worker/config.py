import os

from pydantic import BaseModel


class AwsConfig(BaseModel):
    key_id: str
    key: str
    bucket_input_images: str
    bucket_output_images: str
    endpoint: str

class AppConfig(BaseModel):
    endpoint: str
    temp_file_storage: str
    aws: AwsConfig

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
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_bucket_input_images = os.environ['AWS_BUCKET_NAME_INPUT_IMAGES']
    aws_bucket_output_images = os.environ['AWS_BUCKET_NAME_OUTPUT_IMAGES']
    aws_endpoint = os.environ['AWS_ENDPOINT']
    return AppConfig(
        endpoint=endpoint,
        temp_file_storage=temp_file_storage,
        aws=AwsConfig(
            key_id=aws_access_key_id,
            key=aws_secret_access_key,
            bucket_input_images=aws_bucket_input_images,
            bucket_output_images=aws_bucket_output_images,
            endpoint=aws_endpoint
        )
    )


config = load_from_env()

handler_config = HandlerConfig(
    path_to_data='{}/testA/'.format(os.environ['TEMP_FILE_STORAGE']),
    path_load_model="worker/handler/checkpoints",
    path_test_results='{}/res/'.format(os.environ['TEMP_FILE_STORAGE']),
    image_size=256,
    load_epoch=300,
    switch=True
)
