import os
from box.exceptions import BoxValueError
import yaml
from src.datasetcreation import logger
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
