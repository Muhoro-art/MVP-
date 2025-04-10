# src/backend/services/inventory_service.py

import os
import pandas as pd

def fetch_inventory():
    """
    Reads inventory data from CSV or Database and returns a list/dict.
    For the MVP, we’ll assume CSV read.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to point to your data folder
    data_path = os.path.join(base_dir, '../../../data/cleaned_data.csv')

    
    df = pd.read_csv(data_path)
    # Return as a list of dicts for easy JSON serialization
    return df.to_dict(orient='records')
