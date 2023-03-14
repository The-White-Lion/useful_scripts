import logging
import re
from collections.abc import MutableMapping
from typing import Any, Dict, Iterator
from uuid import uuid4 as uuid


class TweetDict(MutableMapping):
    """Custom dictionary type for Tweet"""

    def __init__(self, tweet: Dict[str, dict]):
        self.logger = logging.getLogger("bookmark.tweetdict")
        self.data = tweet

    def __getitem__(self, key: str) -> Any:
        keys = key.split()
        if len(keys) > 1:
            return self.try_read_key(*keys)
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def try_read_key(self, *args) -> Any:
        """"""
        data = self.data.copy()
        for key in args:
            if isinstance(data, list):
                data = data[0]
            try:
                data = data[key]
            except KeyError:
                self.logger.error("failed to retrieve the key [%s]", key)
                return None

        if isinstance(data, list):
            data = [TweetDict(item) for item in data]
        elif isinstance(data, dict):
            data = TweetDict(data)

        return data


class VideoInfo:
    """Video Information"""

    def __init__(self, tweet: dict):
        self.logger = logging.getLogger("bookmark.video_info")
        # All the required data is stored in the dictionary corresponding to the 'result'
        self.result = TweetDict(tweet)["content itemContent tweet_results result"]
        if self.result is None:
            # The user may have deleted the tweet or the Twitter account associated with the tweet may have been suspended by Twitter, which causes this data to be dirty
            self.logger.error("this item is missing the tweet information [%s]", tweet)
        # It appears that some of the data is nested one more level deeper under the "tweet" key in the "result" dict
        if self.result and self.result.get("tweet", None):
            self.result = TweetDict(self.result["tweet"])

        self.file_type = "video"
        self.video_url = self.get_video_url() if self.result else None
        self.file_name = self.generate_video_name() if self.result else None

    def get_video_url(self) -> str:
        """Get video or animated_gif url from tweet

        Twitter treats Git animated images as video media files.
        """

        media = self.result["legacy extended_entities media"]
        if media is None:
            self.logger.error("original info [%s]", self.result.data)
            return ""
        # From the saved bookmarks, it appears that most of the tweets only contain one video.
        media = media[0]
        if media["type"] == "photo":
            self.file_type = "photo"
            self.logger.info("photo tweet: [%s]", media["expanded_url"])
            return ""

        video = self.get_hd_video(media["video_info variants"])
        video_url = video["url"].split("?")[0]
        return video_url

    def generate_video_name(self) -> str:
        """Generate video name by full text and username"""

        screen_name = self.result["core user_results result legacy screen_name"]
        name = self.result["core user_results result legacy name"]
        full_text = self.result["legacy full_text"]

        if not (full_text and screen_name and name):
            return ""

        full_text = self.remove_illegal_characters(full_text)
        # fulltext could be an empty string
        # Generate a UUID to avoid filename conflicts.
        full_text = full_text if full_text else str(uuid())

        # Remove illegal characters in the name and screen_name
        file_name = self.remove_illegal_characters(f"{name}@{screen_name}{full_text}")
        # The concatenated filename may exceed the system limit, and therefore, may need to be manually truncated
        if len(file_name.encode("utf-8")) > 250:
            file_name = file_name[:80]

        return file_name + ".mp4"

    @staticmethod
    def remove_illegal_characters(text: str) -> str:
        text = re.sub(r"[\r\n]", " ", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r'[ <>:"?.|/*\\]', "", text)
        return text

    @staticmethod
    def get_hd_video(videos: list) -> dict:
        max_bitrate = 0
        hd_video_info = {}
        for video in videos:
            bitrate = video.get("bitrate", 0)
            if bitrate >= max_bitrate:
                max_bitrate = bitrate
                hd_video_info = video.data.copy()

        return hd_video_info

    def __str__(self) -> str:
        return f"推文类型: [{self.file_type}]\n文件名称: [{self.file_name}]\n视频地址: [{self.video_url}]"
