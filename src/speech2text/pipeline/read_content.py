from speech2text import logger
from speech2text.config.configuration import ConfigManager
from speech2text.utils.common import create_directories


class FileRead:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        create_directories([self.config_manager.config.transciptions.base_dir])

    def main(self, file_id, file_content):
        logger.info('MP3 file with ID {file_id} read...')
        yield file_id, file_content