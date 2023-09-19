from src.prediction import logger
from src.prediction.config.configuration import ConfigManager

from src.transcribtiondatasetcreation.pipeline.clean_data import DataCleaner
from src.transcribtiondatasetcreation.pipeline.name_entities_process import NamedEntitiesProcessor

class Cleaner:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

        self._data_cleaner = DataCleaner(config_manager)
        self._named_entity_processor = NamedEntitiesProcessor(config_manager)

    def clean(self, file_id, file_content):
        def generator():
            yield file_id, file_content
        for file_id, content in self._named_entity_processor.main(self._data_cleaner.main(generator())):
            logger.info(f'Data cleaned for ID: {file_id}')
            yield file_id, content