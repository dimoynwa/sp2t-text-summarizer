from prediction import logger
from prediction.config.configuration import ConfigManager
from pathlib import Path

class PredictionSaver:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def save_prediction(self, generator):
        for file_id, prediction in generator:
            base_path = Path(self.config_manager.config.predictions.base_dir, file_id + '.txt')
            with open(base_path, 'w', encoding='utf-8') as f:
                f.write(prediction)
            logger.info(f'Saved file {file_id}.txt')

    def get_prediction(self, file_id):
        base_path = Path(self.config_manager.config.predictions.base_dir, file_id + '.txt')
        if not base_path.exists():
            logger.info(f'{file_id} Not processed yet.')
        else:
            with open(base_path, 'r', encoding='utf-8') as f:
                return f.read()