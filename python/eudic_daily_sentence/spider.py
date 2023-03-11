import logging
import re
import sys
from datetime import date
from typing import Dict

import requests


class Spider:
    """get daily sentence from eudic"""

    daily_sentence_url = "http://dict.eudic.net/home/dailysentence"
    pattern = {
        "en": '<p class="sect sect_en">(.+)</p>',
        "zh": '<p class="sect-trans">(.+)</p>',
        "uuid": "<a href=http://dict.eudic.net/home/dailysentence/(.+) target=_blank>",
    }

    def __init__(self):
        self.logger = logging.getLogger("eudic.spider")

    def get_resp(self) -> requests.Response:
        """get response from eudic daily sentence"""

        try:
            resp = requests.get(self.daily_sentence_url, timeout=5)
        except requests.RequestException as exception:
            self.logger.error("failed to get response: %s", exception)
            sys.exit(1)

        return resp

    def extract_sentence(self, content: str) -> Dict[str, str]:
        """extract sentence that contains chinese and english version from response content"""

        uuid = re.findall(self.pattern["uuid"], content)
        zh_sentence = re.findall(self.pattern["zh"], content)
        eng_sentence = re.findall(self.pattern["en"], content)

        return {
            "_id": uuid[0],
            "zh": zh_sentence[0],
            "en": eng_sentence[0],
            "date": str(date.today()),
        }

    def run(self) -> dict:
        """get daily sentence"""
        resp = self.get_resp()
        content = resp.content.decode("utf-8")
        sentence_data = self.extract_sentence(content)
        return sentence_data
