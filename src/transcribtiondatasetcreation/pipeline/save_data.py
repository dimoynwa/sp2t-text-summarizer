from src.transcribtiondatasetcreation.config.configuration import ConfigManager
from src.transcribtiondatasetcreation import logger
from pathlib import Path

from src.transcribtiondatasetcreation.pipeline.read_data import DataReader
from src.transcribtiondatasetcreation.pipeline.clean_data import DataCleaner
from src.transcribtiondatasetcreation.pipeline.name_entities_process import NamedEntitiesProcessor

class DataSaver:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.clean_data_path = config_manager.config.data.clean_data_dir

    def main(self, content_generator):
        for file_name, content in content_generator:
            file_path = Path(self.clean_data_path, file_name)
            logger.info(f'Saving file {file_path}...')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    cm = ConfigManager()
    data_reader = DataReader(cm)
    data_cleaner = DataCleaner(cm)
    name_entity_processor = NamedEntitiesProcessor(cm)
    data_saver = DataSaver(cm)
    
    data_saver.main(name_entity_processor.main(data_cleaner.main(data_reader.main())))