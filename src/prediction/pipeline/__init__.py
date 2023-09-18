import mlflow
from prediction.utils.common import read_yaml
from prediction.constants import CONFIG_FILE_PATH
from pathlib import Path
from prediction import logger

config = read_yaml(Path(CONFIG_FILE_PATH))

mlflow.set_tracking_uri(config.mlflow.tracking_uri)
logger.info(f'MLFlow initialized with tracking uri: {config.mlflow.tracking_uri}')