import mlflow
from prediction.utils.common import read_yaml
from prediction.constants import CONFIG_FILE_PATH
from prediction.config.configuration import ConfigManager
from pathlib import Path
from prediction import logger

from prediction.pipeline.read_file import Reader
from prediction.pipeline.data_clean import Cleaner
from prediction.pipeline.predictor import Predictor
from prediction.pipeline.save_preiction import PredictionSaver

config = read_yaml(Path(CONFIG_FILE_PATH))

mlflow.set_registry_uri(config.mlflow.tracking_uri)
logger.info(f'MLFlow initialized with tracking uri: {config.mlflow.tracking_uri}')

class PredictionPipeline:
    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self._file_reader = Reader(self.config_manager)
        self._data_cleaner = Cleaner(self.config_manager)
        self._predictor = Predictor(self.config_manager)
        self._data_saver = PredictionSaver(self.config_manager)

    def predict(self, content: str):
        return self._predictor.predict(content)
    
    def predict_async(self, file_id, file):
        content = file.read().decode('utf-8')
        self._data_saver.save_prediction(
            self._predictor.predict_generator(
                self._data_cleaner.clean(file_id, content)
            )
        )

    def get_prediction(self, file_id):
        return self._data_saver.get_prediction(file_id)