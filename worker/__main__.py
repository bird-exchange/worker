import logging
import pathlib
import time

from worker.client.api import app_client
from worker.client.aws import aws_client
from worker.config import config, handler_config
from worker.handler.general import general

logger = logging.getLogger(__name__)


def save_file(file_path: str, file: bytes) -> None:
    pathlib.Path(f'{config.temp_file_storage}/testA').mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb') as f_in:
        f_in.write(file)


def delete_file(file_path: str) -> None:
    pathlib.Path(file_path).unlink()


def main():
    while True:
        bird = app_client.get_task()

        if bird:

            was_fitted = -1
            origin_file_url = app_client.get_origin_file_url(bird.uid)

            if origin_file_url:

                origin_file = aws_client.get_file(origin_file_url)
                origin_file_path = f'{config.temp_file_storage}/testA/{bird.name}'
                save_file(origin_file_path, origin_file)

                general(type_img=bird.type, name_img=bird.name)
                result_file_path = f'{handler_config.path_test_results}{bird.name}'
                result_file = open(result_file_path, 'rb')
                is_upload = app_client.post_file(result_file, bird.name)
                if is_upload:
                    was_fitted = 1
                result_file.close()

                delete_file(origin_file_path)
                delete_file(result_file_path)

            app_client.update_bird(bird, was_fitted)
        time.sleep(3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info('start app')
    main()
