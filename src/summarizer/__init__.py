import os
import logging
import sys

log_string = '[%(asctime)s: %(levelname)s: %(module)s: %(message)s]'
log_dir = 'logs'
log_file = os.path.join(log_dir, 'summarizer.log')

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=log_string,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('summarizer')