from pathlib import Path

from bookmark_parser import BookMarkParser
from logger.logger import config_log
from model import VideoInfo


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
            # 3. 下载视频
            # 4. 保存视频
            print(info)
            print()


if __name__ == "__main__":
    config_log("~/.logs/bookmark/bookmark.log", "bookmark")
    main()
