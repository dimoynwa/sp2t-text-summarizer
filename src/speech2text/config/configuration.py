from speech2text.constants import CONFIG_FILE_PATH
from speech2text.utils.common import read_yaml

class ConfigManager:
    def __init__(self, config_file_path=CONFIG_FILE_PATH) -> None:
        self.config = read_yaml(config_file_path)