import logging
from pathlib import Path
from datetime import date


class Saver:
    """save picture from bytes in memory to disk"""
    file_directory = Path.home() / "Pictures/bing"

    def __init__(self, file_content: bytes, pic_info: dict) -> None:
        self.pic_bytes = file_content
        self.pic_info = pic_info
        self.logger = logging.getLogger("bing_wallpaper.saver")

    def generate_file_name(self) -> str:
        """using today's date and picture copyright info gengrate file name"""
        now_date = date.today()
        file_name = f"{now_date}@{self.pic_info['copyright']}.jpg"
        self.logger.info("picture file name: %s", file_name)
        return file_name

    def save_file(self) -> None:
        file_name = self.generate_file_name()
        file_direcotry = self.file_directory
        file_path = Path(file_direcotry / file_name)
        with open(file_path, "wb") as f:
            f.write(self.pic_bytes.getvalue())
        self.logger.info("wallpaper written successfully")
