# src/backend/controllers/inventory_controller.py

from ..services.inventory_service import fetch_inventory # type: ignore

def get_inventory_data():
    """
    Controller function to process request and return inventory JSON.
    """
    # (Optionally do any extra logic here, e.g., filtering or validation)
    return fetch_inventory()
