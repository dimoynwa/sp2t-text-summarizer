import os
from box.exceptions import BoxValueError
import yaml
from datasetcreation import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path: Path) -> ConfigBox:
    try:
        with open(path, 'r') as f:
            content = yaml.safe_load(f)
            logger.info(f'Yaml {path} loaded successfully.')
            return ConfigBox(content)
    except BoxValueError:
        return ValueError('yaml file is empty')
    
@ensure_annotations
def create_directories(paths: list):
    for path in paths:
        os.makedirs(path, exist_ok=True)
        logger.info(f'created directory: {path}')

@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    with open(path, 'r') as f:
        data = json.load(f)
    logger.info(f'JSON file {path} loaded successfully.')
    return ConfigBox(data)

@ensure_annotations
def save_bin(path: Path, data: Any):
    joblib.dump(data, path)
    logger.info(f'binary file saved in {path}')

@ensure_annotations
def load_bin(path: Path):
    data = joblib.load(path)
    logger.info(f'binary file loaded from {path}')
    return data

@ensure_annotations
def get_slack_auth_token() -> str:
    auth_token = os.environ.get('SLACK_OAUTH_USER_TOKEN')
    auth_token = 'xoxp-484990737874-988535149684-5900317006245-fa666baa22d3a46363b2f5ad068c05fb'
    if not auth_token:
        raise BoxValueError('Please provice SLACK_OAUTH_USER_TOKEN environment variable')
    logger.info(f'SLACK_OAUTH_USER_TOKEN found: {auth_token[:2]}')
    return auth_token
