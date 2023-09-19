from src.transcribtiondatasetcreation.utils.common import read_yaml, create_directories
from src.transcribtiondatasetcreation.constants import CONFIG_FILE_PATH
from pathlib import Path
import os
import sys
import logging

config = read_yaml(Path(CONFIG_FILE_PATH))
create_directories([config.data.summaries_dir, config.data.base_dir, config.data.clean_data_dir])

log_string = '[%(asctime)s: %(levelname)s: %(module)s: %(message)s]'
log_dir = 'logs'
log_file = os.path.join(log_dir, 'transcribtion_dataset_creation_logs.log')

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=log_string,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('transcribtion_dataset_creation')