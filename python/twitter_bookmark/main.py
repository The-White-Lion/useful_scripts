import logging
from pathlib import Path

from logger.logger import config_log
from twitter_bookmark.bookmark_parser import BookMarkParser
from twitter_bookmark.downloader import Downloader
from twitter_bookmark.model import VideoInfo


def main():
    logger = logging.getLogger("bookmark.main")
    file_list = Path("./bookmark").iterdir()
    for bookmark_file in file_list:
        reader = BookMarkParser(bookmark_file)
        data = reader.get_entries()
        for item in data:
            info = VideoInfo(item)
            if info.file_type == "video":
                if info.file_name and info.video_url:
                    downloader = Downloader(info.file_name, info.video_url)
                    try:
                        downloader.save()
                    except Exception as e:
                        logger.error(
                            "An error occurred while saving file [%s]. The reason for [%s] is [%s].",
                            info.file_name,
                            info.video_url,
                            e,
                        )
                print(info)
                print()


if __name__ == "__main__":
    config_log("~/.logs/bookmark/bookmark.log", "bookmark")
    main()
