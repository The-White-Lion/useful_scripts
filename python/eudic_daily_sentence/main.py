import logging
from spider import Spider
from mongo import MongoContextManager
from logger import config_log


def main() -> None:
    logger = logging.getLogger("eudic.main")
    connect_str = "mongodb://lion:lion@127.0.0.1"

    eudic_spider = Spider()
    sentence_data = eudic_spider.run()
    logger.info("sentence: %s", sentence_data)

    with MongoContextManager(connect_str, "python") as mongo:
        result = mongo.create("eudic", sentence_data)
        logger.info("result: %s", result)


if __name__ == "__main__":
    config_log()
    main()
