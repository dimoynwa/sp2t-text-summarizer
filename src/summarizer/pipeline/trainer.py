from src.summarizer import logger
from src.summarizer.config.configuration import ConfigManager

class ModelTrainer:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def train(self, model):
        return model