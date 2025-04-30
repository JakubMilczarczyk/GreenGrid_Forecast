"""This script connect with ENTSO-E API and download data."""
from entsoe import EntsoePandasClient
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class EntsoeParams(BaseModel):
    country_code: str = Field(..., description='ENTSO-E area code')
    start_date: str = Field(..., description='Start date YYYYMMDD foramt')
    end_date: str = Field(..., description='Start date YYYYMMDD foramt')
    output_path: str
    output_format: str = 'parquet'

    @field_validator('output_format')
    def vaildate_format(cls, v):
        if v not in ['csv', 'parquet']:
            raise ValueError('Output format must be csv or parquet')
        return v

def fetch_entsoe_data():
    try:
        token = os.getenv('ENTSOE_API_KEY')
        if not token:
            raise ValueError('ENTSOE_API_KEY not set in environment')
        
        client = EntsoePandasClient(api_key=token)

        tasks = [
            {
                'name': 'total_load',
                'function': client.query_load,
                'params': EntsoeParams(
                    country_code='10YDK-1--------W',
                    start_date='20240101',
                    end_date='20240114',
                    output_path='data/raw/entsoe_generation.parquet',
                ),
            }
        ]

        for task in tasks:
            logger.info(f'Fetching {task["name"]} for {task["params"].country_code}')
            start = pd.Timestamp(task['params'].start_date, tz='Europe/Copenhagen')
            end = pd.Timestamp(task['params'].end_date, tz='Europe/Copenhagen')

            data = task['function'](
                country_code=task['params'].country_code,
                start=start,
                end=end
            )

            if data.empty:
                logger.warning(f'No data returned for {task["name"]}')
                continue

            os.makedirs(os.path.dirname(task['params'].output_path), exist_ok=True)

            if task['params'].output_format == 'parquet':
                data.to_parquet(task['params'].output_path)
            else:
                data.to_csv(task['params'].output_path)
            
            logger.info(f'Saved {task['name']} to {task["params"].output_path}')
    
    except Exception as e:
        logger.exception(f'Error while fetching ENTSO-E data: {e}')

if __name__=='__main__':
    fetch_entsoe_data()
