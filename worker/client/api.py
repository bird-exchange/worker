import logging
from typing import Optional

import httpx
from pydantic.error_wrappers import ValidationError

from worker.config import config
from worker.schemas import Bird

logger = logging.getLogger(__name__)


class AppClient():
    def __init__(self, endpoint: str) -> None:
        self.url = endpoint

    def get_task(self) -> Optional[Bird]:
        response = httpx.get(f'{self.url}/task/')
        if response.status_code == 200:
            try:
                bird = Bird(**response.json())
                return bird
            except ValidationError:
                logger.exception("Server sent invalid data.")
        elif response.status_code == 404:
            logger.info("No task.")
        else:
            logger.exception("Server error.")
        return None

    def get_origin_image_url(self, uid: int) -> Optional[str]:
        response = httpx.get(f'{self.url}/image/origin/{uid}')
        if response.status_code == 200:
            return response.text
        logger.exception("Server doesn't sent image url.")
        return None

    def post_image(self, image: bytes, imagename: str) -> bool:
        upload_url = f'{config.endpoint}/image/result/'
        files = {'file': (imagename, image)}
        answer = httpx.post(upload_url, files=files)
        return answer.status_code == 201

    def update_bird(self, bird: Bird, was_fitted: int) -> None:
        bird_id = bird.dict()['uid']
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        payload = bird.dict()
        payload['was_fitted'] = was_fitted
        updated_bird = Bird(**payload)
        data = updated_bird.json()
        response = httpx.put(f'{self.url}/bird/{bird_id}', data=data, headers=headers)
        if response.status_code != 200:
            logger.exception("Server doesn't update bird.")


app_client = AppClient(config.endpoint)
