import os
import pathlib

from worker.config import config


def draft_handler(file_path: str, filename: str) -> str:
    result_file_path = f'{config.temp_file_storage}/res/{filename}'
    pathlib.Path(f'{config.temp_file_storage}/res').mkdir(parents=True, exist_ok=True)

    os.system(f'cp {file_path} {result_file_path}')

    return result_file_path
