# src/backend/routes/inventory_routes.py

from flask import Blueprint, jsonify, request
from ..controllers.inventory_controller import get_inventory_data

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    """
    GET /inventory
    Returns the current inventory data as JSON.
    """
    inventory_data = get_inventory_data()
    return jsonify(inventory_data), 200

