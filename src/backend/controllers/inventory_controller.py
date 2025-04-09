import pandas as pd
from src.backend.config import DATA_PATH

def get_current_inventory():
    try:
        df = pd.read_csv(DATA_PATH)
        inventory = df[['item_name', 'stock_level']].to_dict(orient='records')
        return inventory
    except Exception as e:
        raise Exception(f"Error reading inventory data: {e}")
