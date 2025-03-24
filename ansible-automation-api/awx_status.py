import requests
from config import AWX_URL
from utils.logger import setup_logger

logger = setup_logger("awx_status")

def check_awx_status():
    url = f"{AWX_URL}/ping/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("AWX is running.")
            return True
        else:
            logger.warning(f"AWX ping returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking AWX status: {e}")
        return False
