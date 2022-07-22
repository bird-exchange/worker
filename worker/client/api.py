import logging
from typing import Optional

import httpx
from pydantic.error_wrappers import ValidationError

from worker.config import config
from worker.schemas import Image

logger = logging.getLogger(__name__)


class AppClient():
    def __init__(self, endpoint: str) -> None:
        self.url = endpoint

    def get_task(self) -> Optional[Image]:
        response = httpx.get(f'{self.url}/task/')
        if response.status_code == 200:
            try:
                image = Image(**response.json())
                return image
            except ValidationError:
                logger.exception("Server sent invalid data.")
        elif response.status_code == 404:
            logger.info("No task.")
        else:
            logger.exception("Server error.")
        return None

    def get_origin_file_url(self, uid: int) -> Optional[str]:
        response = httpx.get(f'{self.url}/files/origin/{uid}')
        if response.status_code == 200:
            return response.text
        logger.exception("Server doesn't sent file url.")
        return None

    def post_file(self, file: bytes, filename: str) -> bool:
        upload_url = f'{config.endpoint}/files/result/'
        files = {'file': (filename, file)}
        answer = httpx.post(upload_url, files=files)
        return answer.status_code == 201

    def update_image(self, image: Image, was_fitted: int) -> None:
        image_id = image.dict()['uid']
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        payload = image.dict()
        payload['was_fitted'] = was_fitted
        updated_image = Image(**payload)
        data = updated_image.json()
        response = httpx.put(f'{self.url}/image/{image_id}', data=data, headers=headers)
        if response.status_code != 200:
            logger.exception("Server doesn't update image.")


app_client = AppClient(config.endpoint)
