import sys
import logging
import requests
from simplejson.errors import JSONDecodeError


class Spider:
    """get request data that is json format from url"""
    base_url = "https://global.bing.com/HPImageArchive.aspx"
    pic_base_url = "https://www.bing.com"
    base_parameters = {
        "format": "js",
        "idx": 0,
        "n": 1,
        "pid": "hp",
        "FORM": "BEHPTB",
        "uhd": 1,
        "uhdwidth": 3840,
        "uhdheight": 2160,
        "setmkt": "zh-Cn",
        "setlang": "zh",
    }
    proxies = {
        "http": "",
        "https": "",
    }
    headers = {}

    def __init__(
        self,
        url: str = base_url,
        parameters: dict = None,
        proxies: dict = None,
        headers: dict = None
    ) -> None:
        if parameters is not None:
            self.base_parameters.update(parameters)
        if proxies is not None:
            self.proxies = proxies
        if headers is not None:
            self.headers = headers

        self.parameters = "&".join([f"{k}={v}" for k, v in self.base_parameters.items()])
        self.url = f"{url}?{self.parameters}"
        self.logger = logging.getLogger("bing_wallpaper.spider")

    def get_resp(self) -> requests.Response:
        """get response based on concatenate url and parameters"""
        self.logger.info("downloading today wallpaper info: %s", self.url)
        self.logger.info("proxies: %s", self.proxies)
        self.logger.info("headers: %s", self.headers)

        try:
            resp = requests.get(self.url, timeout=5, headers=self.headers, proxies=self.proxies)
        except requests.RequestException as exception:
            self.logger.error("wallpaper info download falied: %s", exception)
            sys.exit(1)

        return resp

    def parse_resp(self, resp: requests.Response) -> list:
        """the response that from bing wallpaper api is json format, parse it here"""
        data = []
        if resp.status_code == 200:
            try:
                json_data = resp.json()
            except JSONDecodeError as exception:
                self.logger.error("parse response body faliure: %s", exception)
                self.logger.error("original response body: %s", resp.content)
                sys.exit(1)

            for image_info in json_data["images"]:
                # parameters will effect the quality of picture so discard it
                pic_url = image_info["url"].split("&")[0]
                # '萨塞克斯郡的西欧刺猬，英国 (© Jules Cox/Minden Pictures)' -> 萨塞克斯郡的西欧刺猬，英国
                desc = image_info["copyright"].split("(")[0].strip()
                tmp = {
                    "title": image_info["title"],
                    "copyright": desc,
                    "url": f"{self.pic_base_url}{pic_url}",
                }
                data.append(tmp)
                self.logger.info("orininal picture data: %s", image_info)
                self.logger.info("extract picture data: %s", tmp)

            return data

        self.logger.error("status code error, actual value: %s", resp.status_code)
        self.logger.error("original body: %s", resp.content)
        sys.exit(1)

    def run(self) -> dict:
        resp = self.get_resp()
        pci_data = self.parse_resp(resp)
        return pci_data
