from datasetcreation.config.configuration import ConfigManager
from datasetcreation.pipeline.conversations_stage import ConversationsStage
from datasetcreation.pipeline.replies_stage import RepliesStage
from datasetcreation.pipeline.preprocess_thread import Preprocess
from datasetcreation.pipeline.create_dataset import Dataset

from datasetcreation import logger

class DatasetCreationPipeline:
    def __init__(self) -> None:
        self.config_manager = ConfigManager()

    def create_dataset(self):
        converstation_stage = ConversationsStage(self.config_manager)
        replies_stage = RepliesStage(self.config_manager)
        preprocess_stage = Preprocess(self.config_manager)
        dataset_stage = Dataset(self.config_manager)

        logger.info('Start Dataset creation Pipeline')

        replies = replies_stage.main(converstation_stage.main)
        processed = preprocess_stage.main(replies)
        dataset_stage.main(processed)

        logger.info('End Dataset creation pipeline')