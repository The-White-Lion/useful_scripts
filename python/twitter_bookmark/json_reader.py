import re
import json
from uuid import uuid4 as uuid
from collections.abc import MutableMapping
from typing import Dict, Any, Iterator


class JsonReader:
    """Get data from a JSON file"""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.content = self.read_json_file()

    def read_json_file(self) -> Dict:
        """Read JSON file"""
        content = {}
        with open(self.file_name, "r") as f:
            content = json.load(f)
        return content

    def get_obj_by_params(self, *args) -> Any:
        """Return the dict corresponding to the last positional parameter"""
        data = self.content.copy()
        for arg in args:
            if isinstance(data, list):
                data = data[0]
            if not isinstance(data, dict):
                return []
            data = data[arg]
        return data


class TweetDict(MutableMapping):
    """Custom dictionary type for Tweet"""

    def __init__(self, tweet: dict = None) -> None:
        self.data = tweet if tweet else {}

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

    def try_read_key(self, *args) -> Any:
        """"""
        data = self.data.copy()
        for arg in args:
            if isinstance(data, list):
                data = data[0]
            try:
                data = data[arg]
            except KeyError:
                print(f"不存在子对象 {arg}")
                return None

        if isinstance(data, list):
            data = [TweetDict(item) for item in data]
        elif isinstance(data, dict):
            data = TweetDict(data)   

        return data


class VideoInfo:
    """Video Infomation"""

    def __init__(self, tweet: TweetDict) -> None:
        self.result = tweet["content itemContent tweet_results result"]
        # 有的数据多封装了一层 tweet，需要做处理
        # print(tweet.data)
        if self.result and self.result.get("tweet", None):
            self.result = TweetDict(self.result["tweet"])
        self.video_url = self.get_video_url() if self.result else None
        self.file_name = self.generate_video_name() if self.result else None

    def get_video_url(self) -> str:
        """"""
        medias = self.result["legacy extended_entities media"]
        if medias is None:
            return ""
        # 1. 获取原始尺寸信息
        # original_info = media["original_info"]
        # 从收藏的书签来看，带视频的 tweet 只有一条视频，如果存在多个数据，则表明该书签是图片
        media = medias[0]
        if media["type"] != "video":
            # 此条媒体不是视频，有大问题
            return ""
        # 2. 获取视频列表
        video = self.get_hd_video(media["video_info variants"])

        # 3. 从视频列表中找到质量最高的视频
        video_url = video["url"].split("?")[0]
        return video_url

    def generate_video_name(self) -> str:
        """"""
        screen_name = self.result["core user_results result legacy screen_name"]
        name = self.result["core user_results result legacy name"]
        full_text = self.result["legacy full_text"]

        flag: bool = full_text and screen_name and name
        if not flag:
            return ""

        full_text = self.remove_newlines_and_urls(full_text)
        # full_text 是 tweet 的正文部分，有的用户发布的 tweet 只有图片或者视频，此时生成一个 uuid 作为 full_text
        if full_text == "":
            full_text = str(uuid())
        return f"{screen_name}@{name} {full_text}"
    
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
            if bitrate > max_bitrate:
                max_bitrate = bitrate
                hd_video_info = video.data.copy()

        return hd_video_info

    def __str__(self) -> str:
        return f"视频名称:{self.file_name}\n视频地址:{self.video_url}"


if __name__ == "__main__":
    file_name = "./bookmark/2.json"
    reader = JsonReader(file_name)
    data = reader.get_obj_by_params("data", "bookmark_timeline", "timeline", "instructions", "entries")
    for item in data:
        item = TweetDict(item)
        info = VideoInfo(item)
        print(info)
        print()

