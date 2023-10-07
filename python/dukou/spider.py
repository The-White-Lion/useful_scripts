import logging
import sys
import os

import requests
from requests.exceptions import RequestException


class DukouSpider:
    """dukou vpn daily checkin"""

    header = {
        "origin": "https://dukou.dev",
        "referer": "https://dukou.dev/user/login?redirect=%2F",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }

    proxies = {
        "http": os.getenv("http_proxy"),
        "https": os.getenv("https_proxy"),
    }

    def __init__(self, email: str, passwd: str):
        self.payload = {"email": email, "passwd": passwd}
        self.login_url = "https://dukou.dev/api/token"
        self.checkin_url = "https://dukou.dev/api/user/checkin"
        self.logger = logging.getLogger("dukou.spider")

    def get_access_token(self) -> str:
        """get access token"""
        try:
            resp = requests.post(
                self.login_url,
                data=self.payload,
                headers=self.header,
                proxies=self.proxies,
            )
        except RequestException as exception:
            self.logger.error(
                "An http error occured, the program quit abnormally: %s", exception
            )
            sys.exit(1)

        content = resp.json()
        # login falied
        if content["ret"] != 1:
            self.logger.error("login falied, msg: %s", content["msg"])
            sys.exit(1)

        self.logger.info("login successful: %s", content)
        return content["token"]

    def checkin(self):
        try:
            resp = requests.get(
                self.checkin_url, headers=self.header, proxies=self.proxies
            )
        except RequestException as exception:
            self.logger.error(
                "An http error occured, the program quit abnormally: %s", exception
            )
            sys.exit(1)

        # 接口请求失败的情况下，状态码是正常的，却没有响应体
        if len(resp.content) == 0:
            self.logger.error("checkin falied, please check access-token header")

        self.logger.info("checkin successful, msg: %s", resp.json())

    def run(self):
        token = self.get_access_token()
        self.header["access-token"] = token
        self.logger.info("http headers: %s", self.header)
        self.checkin()
