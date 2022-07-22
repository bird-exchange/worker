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
        image = app_client.get_task()

        if image:

            was_fitted = -1
            origin_file_url = app_client.get_origin_file_url(image.uid)

            if origin_file_url:

                origin_file = aws_client.get_file(origin_file_url)
                origin_file_path = f'{config.temp_file_storage}/testA/{image.name}'
                save_file(origin_file_path, origin_file)

                general(type_img=image.type, name_img=image.name)
                result_file_path = f'{handler_config.path_test_results}{image.name}'
                result_file = open(result_file_path, 'rb')
                is_upload = app_client.post_file(result_file, image.name)
                if is_upload:
                    was_fitted = 1
                result_file.close()

                delete_file(origin_file_path)
                delete_file(result_file_path)

            app_client.update_image(image, was_fitted)
        time.sleep(3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info('start app')
    main()
