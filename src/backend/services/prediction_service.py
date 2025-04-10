# src/backend/services/prediction_service.py

import os
import pandas as pd
import datetime
from ...predict_inventory import predict_inventory  # <-- Import from your existing script

def forecast_stock(date_str):
    """
    1. Prepare a sample input row
    2. Update the 'date' and possibly 'delivery_time'
    3. Call your existing predict_inventory() function
    """
    # Validate date format
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Got: {date_str}")

    # Load a sample row from CSV (or build from scratch) 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../../../data/cleaned_data.csv')
    df = pd.read_csv(data_path)
    sample_row = df.iloc[[0]].copy()

    # Update the date and delivery_time
    sample_row['date'] = date_str
    sample_row['delivery_time'] = (date_obj + datetime.timedelta(days=10)).strftime("%Y-%m-%d")

    # Call your existing function from predict_inventory.py
    # This function should load the model, reindex features, etc.
    prediction = predict_inventory(sample_row)
    return float(prediction[0])  # Convert numpy.float64 to float
