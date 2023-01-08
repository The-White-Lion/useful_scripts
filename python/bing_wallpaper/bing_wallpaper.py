import logging
from spider import Spider
from saver import Saver
from downloader import Downloader
from logger import config_log


def main() -> None:
    config_log()
    logger = logging.getLogger("bing_wallpaper.main")
    logger.info("start getting today bing wallpaper infomation =========================")

    bing_spider = Spider()
    pic_data = bing_spider.run()
    logger.info("start downloading today wallpaper =========================")
    for pic in pic_data:
        downloader = Downloader(pic["url"])
        pic_bytes = downloader.run()
        saver = Saver(pic_bytes, pic)
        saver.save_file()

    logger.info("today wallpaper download done =========================")


if __name__ == "__main__":
    main()
