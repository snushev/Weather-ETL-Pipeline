import pandas as pd
from loguru import logger
from datetime import datetime


def process_data(data):
    if not data:
        logger.error("Invalid or empty data received for processing.")
        return None

    try:
        df = pd.DataFrame()

        df['weather'] = data['weather'][0]['main']
        df['description'] = data['weather'][0]['description']
        df['humidity'] = data['main']['humidity']
        df['pressure'] = data['main']['pressure']
        df['wind_speed'] = data['wind']['speed']
        df['sunrise'] = pd.to_datetime(data['sys']['sunrise'], unit='s') + pd.Timedelta(hours=2)
        df['sunset'] = pd.to_datetime(data['sys']['sunset'], unit='s') + pd.Timedelta(hours=2)
        df['timestamp'] = pd.to_datetime(data['dt'], unit='s') + pd.Timedelta(hours=2)
        df['time_added'] = pd.to_datetime(datetime.now())

        logger.info("Processed data successfully.")

        return df

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Error processing data: {e}")
        return None
