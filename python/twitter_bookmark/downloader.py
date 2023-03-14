import logging
from pathlib import Path

import requests


class Downloader:
    """"""

    def __init__(self, file_name: str, url: str):
        self.file_name = file_name
        self.url = url
        self.logger = logging.getLogger("bookmark.downloader")

    def download(self) -> requests.Response:
        # Todo 下载失败重试
        resp = requests.Response()
        try:
            resp = requests.get(self.url, timeout=15, stream=True)
            resp.raise_for_status
        except requests.RequestException as e:
            self.logger.error(
                "failed to download video file: [%s] due to [%s]", self.file_name, e
            )
        finally:
            return resp

    def save(self, directory: str = "video"):
        self.check_or_mkdir(directory)

        self.logger.info("Starting to save the file [%s]", self.file_name)
        resp = self.download()
        resp.raise_for_status()
        with resp as r:
            with open(f"{directory}/{self.file_name}", "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
        self.logger.info("The file [%s] is completely saved", self.file_name)

    @staticmethod
    def check_or_mkdir(directory: str):
        directory_path = Path(directory).expanduser()
        if not directory_path.exists():
            directory_path.mkdir(parents=True)
