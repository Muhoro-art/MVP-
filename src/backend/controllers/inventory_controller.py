# src/backend/controllers/inventory_controller.py

from ..services.inventory_service import fetch_inventory, fetch_inventory_summary, fetch_reorder_plan # type: ignore

def get_inventory_data():
    """
    Controller function to process request and return inventory JSON.
    """
    # (Optionally do any extra logic here, e.g., filtering or validation)
    return fetch_inventory()


def get_inventory_summary():
    return fetch_inventory_summary()


def get_reorder_plan(horizon_days=14, safety_days=2, lookback_days=60):
    return fetch_reorder_plan(
        horizon_days=horizon_days,
        safety_days=safety_days,
        lookback_days=lookback_days,
    )
