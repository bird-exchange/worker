import logging
import pathlib
import time

from worker.client.api import app_client
from worker.client.aws import aws_client
from worker.config import config, handler_config
from worker.handler.general import general

logger = logging.getLogger(__name__)


def save_image(image_path: str, image: bytes) -> None:
    pathlib.Path(f'{config.temp_file_storage}/testA').mkdir(parents=True, exist_ok=True)
    with open(image_path, 'wb') as f_in:
        f_in.write(image)


def delete_image(image_path: str) -> None:
    pathlib.Path(image_path).unlink()


def main():
    while True:
        bird = app_client.get_task()

        if bird:

            was_fitted = -1

            origin_image_name = bird.name
            aws_client.download_image_by_name(
                filename=origin_image_name,
                bucket='input-images',
                file_storage=f'{config.temp_file_storage}/testA/'
            )
            origin_image_path = f'{config.temp_file_storage}/testA/{bird.name}'

            general(type_img=bird.type, name_img=bird.name)

            result_image_path = f'{handler_config.path_test_results}{bird.name}'
            result_image = open(result_image_path, 'rb')
            is_upload = app_client.post_image(result_image, bird.name)
            if is_upload:
                was_fitted = 1
            result_image.close()

            delete_image(origin_image_path)
            delete_image(result_image_path)

            app_client.update_bird(bird, was_fitted)
        time.sleep(3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info('start app')
    main()
