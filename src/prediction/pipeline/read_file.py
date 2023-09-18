from prediction import logger
from prediction.config.configuration import ConfigManager

class Reader:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def read(self, file):
        file_content = file.read()
        yield file_content

    