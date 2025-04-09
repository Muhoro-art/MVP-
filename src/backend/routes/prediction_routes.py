from flask import Blueprint
from src.backend.controllers.prediction_controller import get_prediction

prediction_bp = Blueprint("prediction_bp", __name__)

prediction_bp.route("/predict", methods=["GET"])(get_prediction)
