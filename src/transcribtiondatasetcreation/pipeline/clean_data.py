from transcribtiondatasetcreation.config.configuration import ConfigManager
from transcribtiondatasetcreation import logger
from transcribtiondatasetcreation.components.text_cleaner import clean_text
from transcribtiondatasetcreation.pipeline.read_data import DataReader

class DataCleaner:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
    
    def main(self, content_generator):
        for file_path, content in content_generator:
            logger.info(f'Cleaning file {file_path}...')
            yield file_path, clean_text(content)

if __name__ == '__main__':
    cm = ConfigManager()
    data_reader = DataReader(cm)
    data_cleaner = DataCleaner(cm)

    for file_path, content in data_cleaner.main(data_reader.main()):
        logger.info(f'Data clened for file {file_path}: {content}')
