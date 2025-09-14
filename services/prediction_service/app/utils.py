import os
from config import logger

def validate_path(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f'Path does not exist {path}')
    return path

def preprocess_input(features: list[float]) -> list[float]:
    # Placeholder for actual preprocessing logic
    logger.info('Preprocessing input features')
    return features
