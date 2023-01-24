import logging
from pathlib import Path
from spider import DukouSpider
from logger.logger import config_log
from yaml_reader import YAMLReader


def main():
    logger = logging.getLogger("dukou.main")
    logger.info("==========开始每日签到==========")
    reader = YAMLReader("config.yaml")
    account_data = reader.read_config()
    index = 1
    for account in account_data:
        logger.info("==========签到第 %s 个账号==========", index)
        dukou = DukouSpider(account["email"], account["passwd"])
        dukou.run()
        index += 1
    logger.info("==========签到完成==========")


if __name__ == "__main__":
    config_log(Path(Path.home() / ".logs/dukou/dukou.log"), "dukou")
    main()
