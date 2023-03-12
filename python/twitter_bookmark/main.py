from pathlib import Path

from logger.logger import config_log
from twitter_bookmark.bookmark_parser import BookMarkParser
from twitter_bookmark.downloader import Downloader
from twitter_bookmark.model import VideoInfo


def main():
    # 1. 获取所有书签文件
    file_list = Path("./bookmark").iterdir()
    for bookmark_file in file_list:
        # 2. 解析书签
        print(f"当前文件为:{bookmark_file}")
        reader = BookMarkParser(bookmark_file)
        data = reader.get_entries()
        for item in data:
            info = VideoInfo(item)
            if info.file_type == "video":
                # 3. 下载视频
                if info.file_name and info.video_url:
                    downloader = Downloader(info.file_name, info.video_url)
                    downloader.save()
                # 4. 保存视频
            print(info)
            print()


if __name__ == "__main__":
    config_log("~/.logs/bookmark/bookmark.log", "bookmark")
    main()
