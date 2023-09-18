import os
import sys
import logging

log_string = '[%(asctime)s: %(levelname)s: %(module)s: %(message)s]'
log_dir = 'logs'
log_file = os.path.join(log_dir, 'dataset_creation_logs.log')

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=log_string,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('mlflow_demo')