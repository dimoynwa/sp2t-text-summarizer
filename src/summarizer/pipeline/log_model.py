from summarizer import logger
from summarizer.config.configuration import ConfigManager
from pathlib import Path

import mlflow
import dagshub
import time

class MlFlowLogger:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        dagshub.init(self.config_manager.config.dagshub.repo, self.config_manager.config.dagshub.user, mlflow=True)
        mlflow.set_tracking_uri(self.config_manager.config.mlflow.tracking_uri)

    def log_model(self, pipe, scores):
        logger.info(f'Logging model with name {self.config_manager.config.model.name} to {self.config_manager.config.mlflow.tracking_uri}')
        with mlflow.start_run():
            mlflow.log_metrics(scores)
            mlflow.log_params(self.config_manager.config.model)

            # Define an inference_config
            inference_config = {
                "max_length": self.config_manager.config.model.max_length,
                "min_length": self.config_manager.config.model.min_length,
                "truncation": self.config_manager.config.model.truncation
            }

            if self.config_manager.config.mlflow.log_model:
                mlflow.transformers.log_model(pipe,
                                  artifact_path = self.config_manager.config.model.name + str(time.time()),
                                  inference_config=inference_config,
                                  registered_model_name = self.config_manager.config.mlflow.registered_model_name)

            # Saving inference_config with the model
            mlflow.transformers.save_model(
                pipe,
                path=Path(self.config_manager.config.mlflow.local_dir, self.config_manager.config.model.name + str(time.time())),
                inference_config=inference_config
            )
    