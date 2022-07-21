import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class AWSClient():
    def get_file(self, url: str) -> Optional[bytes]:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.content
        logger.exception("File could not be loaded.")
        return None


aws_client = AWSClient()
