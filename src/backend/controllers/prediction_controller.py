from flask import request, jsonify
from src.backend.services.prediction_service import predict_inventory

def get_prediction():
    try:
        day = request.args.get("day", type=int)
        if day is None:
            return jsonify({"error": "Missing 'day' query parameter."}), 400

        prediction = predict_inventory(day)
        return jsonify({"Прогнозируемый запас": prediction}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
