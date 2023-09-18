from transcribtiondatasetcreation.config.configuration import ConfigManager
from transcribtiondatasetcreation import logger
from transcribtiondatasetcreation.components.text_cleaner import name_entity_process

from transcribtiondatasetcreation.pipeline.read_data import DataReader
from transcribtiondatasetcreation.pipeline.clean_data import DataCleaner

class NamedEntitiesProcessor:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        
        self.person_names = []

    def main(self, content_generator):
        for file_path, content in content_generator:
            logger.info(f'Processing names in file {file_path}...')
            yield file_path, name_entity_process(content)
            
if __name__ == '__main__':
    cm = ConfigManager()
    data_reader = DataReader(cm)
    data_cleaner = DataCleaner(cm)
    name_entity_processor = NamedEntitiesProcessor(cm)

    for file_path, content in name_entity_processor.main(data_cleaner.main(data_reader.main())):
        logger.info(f'Named entities processed {file_path}: {content}')