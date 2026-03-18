# src/backend/routes/inventory_routes.py

from flask import Blueprint, jsonify, request
from ..controllers.inventory_controller import get_inventory_data, get_inventory_summary, get_reorder_plan

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    """
    GET /inventory
    Returns the current inventory data as JSON.
    """
    inventory_data = get_inventory_data()
    return jsonify(inventory_data), 200


@inventory_bp.route('/summary', methods=['GET'])
def inventory_summary():
    """
    GET /inventory/summary
    Returns latest stock status per item.
    """
    return jsonify(get_inventory_summary()), 200


@inventory_bp.route('/reorder-plan', methods=['GET'])
def reorder_plan():
    """
    GET /inventory/reorder-plan?horizon_days=14&safety_days=2&lookback_days=60
    Returns practical reorder recommendations.
    """
    try:
        horizon_days = int(request.args.get('horizon_days', 14))
        safety_days = int(request.args.get('safety_days', 2))
        lookback_days = int(request.args.get('lookback_days', 60))
    except ValueError:
        return jsonify({"error": "horizon_days, safety_days, and lookback_days must be integers."}), 400

    if horizon_days < 1 or safety_days < 0 or lookback_days < 1:
        return jsonify({"error": "Invalid planning parameters."}), 400

    plan = get_reorder_plan(
        horizon_days=horizon_days,
        safety_days=safety_days,
        lookback_days=lookback_days,
    )
    return jsonify(plan), 200

