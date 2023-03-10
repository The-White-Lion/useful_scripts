from parser import BookMarkParser

from logger.logger import config_log
from model import VideoInfo


def main():
    # 1. 获取所有书签文件
    # 2. 解析所有的书签
    # 3. 下载视频
    # 4. 保存视频
    file_name = "./1.json"
    reader = BookMarkParser(file_name)
    data = reader.get_entries()
    for item in data:
        info = VideoInfo(item)
        print(info)
        print()


if __name__ == "__main__":
    config_log("~/.logs/boormark/bookmark.log", "bookmark")
    main()
