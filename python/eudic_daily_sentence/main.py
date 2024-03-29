import logging

from eudic_daily_sentence.mongo import MongoContextManager
from eudic_daily_sentence.spider import Spider
from logger.logger import config_log


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
    daily_log = os.getenv("DAILY_LOG", "~/.logs/eudic/daily_sentence.log")
    config_log(dialy_log, "eudic")
    main()
