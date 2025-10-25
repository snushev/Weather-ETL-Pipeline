import requests
from app import config
from loguru import logger
from datetime import datetime


def fetch_data():
    try:
        if not config.API_URL:
            raise ValueError("API_URL is not set in environmetn variables.")

        parameters = {
            "lat": config.LAT,
            "lon": config.LON,
            "appid": config.API_KEY,
            "units": "metric",
            "cng": 4
        }

        response = requests.get(config.API_URL, params=parameters, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetch data for date: {datetime.now()}")
        return data
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
