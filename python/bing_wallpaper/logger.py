import logging
from pathlib import Path


def mkdir_log_directory() -> Path:
    log_directory = Path(Path.home() / ".logs/bing_wallpaper")
    if not log_directory.exists():
        log_directory.mkdir(parents=True)

    return log_directory


def touch_log_file(directory: Path) -> Path:
    log_file = Path(directory / "bing_wallpaper.log")
    log_file.touch()
    return log_file


def config_log() -> None:
    """config log, contains handler, formatter etc."""
    log_directory = mkdir_log_directory()
    log_file = touch_log_file(log_directory)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format_str = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format_str)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)


logger = logging.getLogger("bing_wallpaper")
