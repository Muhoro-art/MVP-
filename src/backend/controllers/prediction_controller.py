# src/backend/controllers/prediction_controller.py

from ..services.prediction_service import forecast_stock

def get_prediction(date_str):
    """
    Controller-level logic for handling the query parameters and calling the service.
    """
    # Validate date format or do any other pre-processing
    # ...
    # Pass it to the service
    return forecast_stock(date_str)
