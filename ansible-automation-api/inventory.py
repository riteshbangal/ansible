import requests
from config import AWX_URL
from utils.logger import setup_logger
from auth import get_awx_token

logger = setup_logger("inventory")

def validate_inventory(inventory_id):
    token = get_awx_token()
    if not token:
        logger.error("Failed to retrieve token. Inventory check aborted.")
        return

    url = f"{AWX_URL}/inventories/{inventory_id}/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        inventory = response.json()
        logger.info(f"Inventory {inventory_id} found: {inventory['name']}")
        return inventory
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching inventory: {e}")
        return None
