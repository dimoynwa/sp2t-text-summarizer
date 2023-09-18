import pandas as pd
from datasetcreation.config.configuration import ConfigManager
from datasetcreation import logger
from datasetcreation.constants import CSV_DELIMITER
from ensure import ensure_annotations
from datasetcreation.utils.common import create_directories
from pathlib import Path
from datasetcreation.pipeline.preprocess_thread import Preprocess

STAGE_NAME = 'Create dataset'

class Dataset:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.base_dir = config_manager.config.dataset.base_dir
        self.file_name = config_manager.config.dataset.file_name

    @ensure_annotations
    def main(self, text_generator):
        create_directories([self.base_dir])
        df = pd.DataFrame(text_generator, columns=['channel', 'ts', 'conversation'])
        path = Path(self.base_dir, self.file_name)
        logger.info(f'Save dataset to file {path}')
        df.to_csv(path, sep=CSV_DELIMITER)



if __name__ == '__main__':
    config_manager = ConfigManager()
    
    dataset_path = Path(config_manager.config.dataset.base_dir, config_manager.config.dataset.file_name)

    df = pd.read_csv(dataset_path, sep=CSV_DELIMITER)

    def test_generator():
        # Iterate over rows
        for _, row in df.iterrows():
            yield row['channel'], row['ts'], row['conversation']

    preprocess = Preprocess(config_manager)

    stage = Dataset(config_manager)
    stage.main(preprocess.main(test_generator()))