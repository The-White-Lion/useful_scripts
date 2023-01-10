import sys
import logging
from io import BytesIO
import requests


class Downloader:
    """download picture with given url and save it to file"""

    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = logging.getLogger("bing_wallpaper.downloader")

    def download(self) -> requests.Response:
        try:
            resp = requests.get(self.url, timeout=5, stream=True)
        except requests.RequestException as exception:
            self.logger.error("wallpaper picture download falied: %s", exception)
            sys.exit(1)

        return resp

    def run(self) -> None:
        """download picture"""
        resp = self.download()
        if resp.status_code == 200:
            # attempt using stream to complete saving file
            pic_bytes = BytesIO()
            for chunk in resp.iter_content(chunk_size=1024*1024):
                pic_bytes.write(chunk)

            return pic_bytes
        self.logger.error("status code error，actual value: %s", resp.status_code)
        self.logger.error("original body: %s", resp.content)
        sys.exit(1)
