import logging
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    data_dir: Path
    models_dir: Path
    config_dir: Path
    service_port: int = 8000
    log_level: str = "INFO"

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'

settings = Settings()

logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getlogger('prediction-service')

logger.info('Loaded settings:')
logger.info(f'DATA_DIR={settings.data_dir}')
logger.info(f'MODELS_DIR={settings.models_dir}')
logger.info(f'CONFIG_DIR={settings.config_dir}')
logger.info(f'LOG_LEVEL={settings.log_level}')
