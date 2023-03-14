import json
import logging
from pathlib import Path
from typing import Dict, List


class BookMarkParser:
    """Get the list of contents from a bookmark file"""

    def __init__(self, file_name: Path):
        self.logger = logging.getLogger("bookmark.parser")
        self.file_name = file_name
        self.content = self.read_json_file()

    def read_json_file(self) -> Dict[str, dict]:
        """Read JSON file"""

        content = {}
        with self.file_name.open("r") as f:
            content = json.load(f)
        return content

    def get_entries(self) -> List[dict]:
        """Get entries from bookmark
        The "entries" is a list containing the contents of tweets.

        :return: entries list
        """

        keys = ("data", "bookmark_timeline", "timeline", "instructions", "entries")
        for key in keys:
            if isinstance(self.content, list):
                self.content = self.content[0]
            try:
                self.content = self.content[key]
            except KeyError as e:
                self.logger.error("bookmark file [%s] parse failure", self.file_name)
                self.logger.error("error message [%s]", e)
                return []
        if not isinstance(self.content, list):
            self.logger.error(
                "failed to retrieve 'entries' list from bookmark file [%s]",
                self.file_name,
            )
            return []
        return self.content.copy()
