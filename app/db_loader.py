import psycopg2
from psycopg2.extras import execute_values
from loguru import logger
from app import config


def get_connection():
    """Connect to the PostgreSQL server"""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


def create_table():
    """Create table if it doesn't exist"""

    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("""
    CREATE TABLE IF NOT EXISTS current_temperature (
        id SERIAL PRIMARY KEY,
        weather VARCHAR(100),
        description VARCHAR(100),
        humidity FLOAT,
        pressure FLOAT,
        wind_speed FLOAT,
        sunrise TIMESTAMP,
        sunset TIMESTAMP,
        timestamp TIMESTAMP,
        time_added TIMESTAMP
        );
    """)
        conn.commit()
    conn.close()
    logger.info("Table 'current_temperature' is ready")


def load_to_db(df):
    if df is None:
        logger.warning("No data to insert")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            records = df.values.tolist()
            execute_values(cur, """
                INSERT INTO current_temperature (
                            weather,
                            description,
                            humidity,
                            pressure,
                            wind_speed,
                            sunrise,
                            sunset,
                            timestamp,
                            time_added
                            )
                            VALUES %s
                            """, records)
            conn.commit()
        logger.info(f"Inserted {len(df)} records into database.")
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()
