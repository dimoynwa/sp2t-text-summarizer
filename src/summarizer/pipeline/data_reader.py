import os
from pathlib import Path
from summarizer import logger
from summarizer.config.configuration import ConfigManager
from ensure import ensure_annotations

class DataReader:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def main(self):
        data_dir = self.config_manager.config.data.clean_data_dir
        summaries_dir = self.config_manager.config.data.summaries_dir
        texts = self._read_folder(data_dir)
        reference_summaries = self._read_folder(summaries_dir)

        assert len(texts) == len(reference_summaries)

        return texts, reference_summaries

    @ensure_annotations
    def _read_folder(self, folder_path: str) -> list:
        logger.info(f'Read folder {folder_path}')
        files = Path(folder_path).glob('*')
        def read_file(f):
            logger.info(f'Reading file {f}...')
            with open(f, 'r', encoding='utf-8') as f:
                return f.read()
        return [read_file(f) for f in files]
    
if __name__ == '__main__':
    cm = ConfigManager()
    data_reader = DataReader(cm)
    texts, reference_summaries = data_reader.main()
    logger.info(f'Read {len(texts)} texts and {len(reference_summaries)} summaries')