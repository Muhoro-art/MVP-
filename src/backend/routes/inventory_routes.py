from flask import Blueprint, jsonify
from src.backend.controllers.inventory_controller import get_current_inventory

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def inventory():
    try:
        inventory_data = get_current_inventory()
        return jsonify(inventory_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
