from transcribtiondatasetcreation.config.configuration import ConfigManager
from transcribtiondatasetcreation import logger
from pathlib import Path

class DataReader:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def main(self):
        base_dir = self.config_manager.config.data.base_dir
        files = Path(base_dir).glob('*')
        for file in files:
            logger.info(f'Reading file {file}...')
            with open(file, 'r', encoding='utf-8') as f:
                yield file.name, f.read()

if __name__ == '__main__':
    cm = ConfigManager()
    reader = DataReader(cm)
    for message in reader.main():
        print(f'Message with length read {len(message)}')