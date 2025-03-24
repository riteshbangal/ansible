import requests
import json
from config import AWX_URL, AWX_ADMIN_USER, AWX_ADMIN_PASSWORD
from utils.logger import setup_logger

logger = setup_logger("auth")

def get_awx_token():
    url = f"{AWX_URL}/tokens/"
    payload = {"username": AWX_ADMIN_USER, "password": AWX_ADMIN_PASSWORD}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        token = response.json().get("token")
        logger.info("AWX Token retrieved successfully.")
        return token
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching AWX token: {e}")
        return None
