# src/backend/routes/prediction_routes.py

from flask import Blueprint, jsonify, request
from ..controllers.prediction_controller import get_prediction

prediction_bp = Blueprint('prediction_bp', __name__)

@prediction_bp.route('/', methods=['GET'])
def predict_inventory():
    """
    GET /predict?date=YYYY-MM-DD
    Returns a forecast of the inventory level for the specified date.
    """
    input_date = request.args.get('date')
    if not input_date:
        return jsonify({"error": "Missing 'date' query parameter."}), 400

    try:
        prediction = get_prediction(input_date)
        return jsonify({
            "date": input_date,
            "predicted_stock": prediction
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error."}), 500
