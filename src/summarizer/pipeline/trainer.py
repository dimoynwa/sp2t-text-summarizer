from summarizer import logger
from summarizer.config.configuration import ConfigManager

class ModelTrainer:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def train(self, model):
        return model