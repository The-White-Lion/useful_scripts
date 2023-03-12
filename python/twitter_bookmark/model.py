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
        self.logger = logging.getLogger("bookmark.video")
        # 所有需要的数据都在 result 对应的字典中存放
        self.result = TweetDict(tweet)["content itemContent tweet_results result"]
        if self.result is None:
            # 该数据缺少推文信息，需要处理
            self.logger.error("this item is missing the tweet information [%s]", tweet)
        # 有的数据多封装了一层 tweet，需要做处理
        if self.result and self.result.get("tweet", None):
            self.result = TweetDict(self.result["tweet"])
        self.file_type = "video"
        self.video_url = self.get_video_url() if self.result else None
        self.file_name = self.generate_video_name() if self.result else None

    def get_video_url(self) -> str:
        """"""
        media = self.result["legacy extended_entities media"]
        if media is None:
            self.logger.error("orininal info [%s]", self.result.data)
            return ""
        # 从收藏的书签来看，带视频的 tweet 只有一条视频，如果存在多个数据，则表明该书签是图片
        media = media[0]
        # animated_gif video photo
        # 根据 type 获取对应的 url
        file_type = media["type"]
        if file_type == "photo":
            self.file_type = "photo"
            # Todo 记录该 tweet 信息
            return media["expanded_url"]
        # twitter 将 gif 当作视频处理，此处可以使用相同的方法
        # 3. 从视频列表中找到质量最高的视频
        video = self.get_hd_video(media["video_info variants"])
        video_url = video["url"].split("?")[0]
        return video_url

    def generate_video_name(self) -> str:
        """"""
        screen_name = self.result["core user_results result legacy screen_name"]
        name = self.result["core user_results result legacy name"]
        full_text = self.result["legacy full_text"]

        if not (full_text and screen_name and name):
            return ""

        full_text = self.remove_newlines_and_urls(full_text)
        # full_text 是 tweet 的正文部分，有的用户发布的 tweet 只有图片或者视频，此时生成一个 uuid 作为
        # full_text
        if full_text == "":
            full_text = str(uuid())
        return f"{name}@{screen_name}{full_text}.mp4".replace(" ", "_")

    @staticmethod
    def remove_newlines_and_urls(text: str) -> str:
        text = re.sub(r"[\r\n]", " ", text)
        text = re.sub(r"http\S+", "", text)
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
        return f"推文类型:{self.file_type}\n视频名称:{self.file_name}\n视频地址:{self.video_url}"
