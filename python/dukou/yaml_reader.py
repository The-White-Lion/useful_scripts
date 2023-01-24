import sys
import logging
import yaml


class YAMLReader:
    """Read account config from YAML file"""

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.logger = logging.getLogger("dukou.reader")

    def get_file_content(self) -> str:
        """Read file content"""
        self.logger.info("read config file content %s", self.config_file)
        with open(self.config_file, "r", encoding="utf-8",) as file:
            content = file.read()

        if len(content) == 0:
            self.logger.error("config file error, there is nothing data")
            sys.exit(1)
        return content

    def _schema_validation(self, content: dict) -> None:
        """Schema Validation, config file format must be like this
            account:
                -
                    email: example@github.com
                    passwd: your_passwd
        """
        if not content["account"]:
            self.logger.error("config format error please check it")
            sys.exit(1)

        for account in content["account"]:
            if not (account["email"] and account["passwd"]):
                self.logger.error("maybe you forgot to fill email or passwd")
                sys.exit(1)

    def read_config(self) -> dict:
        """Parse the YAML document to the corresponding Python object"""
        file_content = self.get_file_content()
        yaml_content = yaml.safe_load(file_content)
        self._schema_validation(yaml_content)

        return yaml_content["account"]
