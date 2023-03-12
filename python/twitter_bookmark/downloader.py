import contextlib
import logging

import requests


class Downloader:
    """"""

    def __init__(self, file_name: str, url: str):
        self.file_name = file_name
        self.url = url
        self.logger = logging.getLogger("bookmark.downloader")

    def download(self) -> requests.Response:
        resp = requests.Response()
        try:
            resp = requests.get(self.url, timeout=15, stream=True)
        except requests.RequestException as e:
            self.logger.error(
                "falied to download video file: [%s] due to [%s]", self.file_name, e
            )
        finally:
            return resp

    def save(self):
        resp = self.download()
        with open(self.file_name, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
