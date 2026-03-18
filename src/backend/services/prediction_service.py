# src/backend/services/prediction_service.py

import os
import pandas as pd
import datetime
from ...predict_inventory import predict_inventory  # <-- Import from your existing script

def forecast_stock(date_str, item=None):
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

    # Load historical rows from CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../../../data/cleaned_data.csv')
    df = pd.read_csv(data_path)

    if item:
        matching = df[df['item'].str.lower() == item.lower()]
        if matching.empty:
            raise ValueError(f"Item not found: {item}")
        sample_row = matching.tail(1).copy()
        lead_days = (pd.to_datetime(matching['delivery_time']) - pd.to_datetime(matching['date'])).dt.days.clip(lower=0)
        avg_lead_days = int(lead_days.mean()) if not lead_days.empty else 10
    else:
        sample_row = df.tail(1).copy()
        avg_lead_days = 10

    # Update the date and delivery_time
    sample_row['date'] = date_str
    sample_row['delivery_time'] = (date_obj + datetime.timedelta(days=avg_lead_days)).strftime("%Y-%m-%d")

    # Call your existing function from predict_inventory.py
    # This function should load the model, reindex features, etc.
    prediction = predict_inventory(sample_row)
    return float(prediction[0])  # Convert numpy.float64 to float
