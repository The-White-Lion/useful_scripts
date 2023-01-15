import logging
from pathlib import Path


def mkdir_log_directory(log_file: Path) -> bool:
    log_directory = Path(log_file.parent)
    if not log_directory.exists():
        log_directory.mkdir(parents=True)

    return True


def touch_log_file(log_file: Path) -> bool:
    if not log_file.exists():
        log_file.touch()

    return True


def config_log(log_file: Path, logger_name: str) -> None:
    """config log output, contains handler, formatter etc."""
    mkdir_log_directory(log_file)
    touch_log_file(log_file)

    logger = logging.getLogger(logger_name)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format_str = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format_str)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
