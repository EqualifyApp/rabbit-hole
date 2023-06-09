import os
import logging
from data.access import connection

# Add logging to each file with
#   from utils.watch import logger


# Set up logger: "A11yLogger"
logger = logging.getLogger("A11y🪵 ")

# Check if logger already has handlers
if not logger.hasHandlers():
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
    logger.setLevel(logging.getLevelName(log_level))

    # Create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.getLevelName(log_level))

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

def configure_logger():
    # Use the logger from logging_config.py
    global logger
    logger = logging.getLogger("A11y🪵 ")


def test_database():
    logger.debug('Testing Database Connection')
    conn = connection()
    conn.open()
    try:
        conn.cur.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE datname = 'a11ydata';")
        result = conn.cur.fetchone()[0]
        if result >= 1:
            return True
        else:
            return False
    except:
        return False
    finally:
        conn.close()