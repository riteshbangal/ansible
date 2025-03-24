from awx_status import check_awx_status
from inventory import validate_inventory

if __name__ == "__main__":
    # 1️⃣ Check AWX status
    if not check_awx_status():
        print("AWX is not running. Exiting.")
        exit(1)

    # 2️⃣ Validate inventory
    inventory_id = 2  # Replace with your actual inventory ID
    inventory = validate_inventory(inventory_id)
    if not inventory:
        print(f"Inventory {inventory_id} not found.")
