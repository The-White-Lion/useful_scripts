import logging

from logger.logger import config_log
from mongo import MongoContextManager
from spider import Spider


def main():
    logger = logging.getLogger("eudic.main")
    connect_str = "mongodb://lion:lion@192.168.0.103"

    eudic_spider = Spider()
    sentence_data = eudic_spider.run()
    logger.info("sentence: %s", sentence_data)

    with MongoContextManager(connect_str, "python") as mongo:
        result = mongo.create("eudic", sentence_data)
        logger.info("result: %s", result)


if __name__ == "__main__":
    config_log("~/.logs/eudic/daily_sentence.log", "eudic")
    main()
