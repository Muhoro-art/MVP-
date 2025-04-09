import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../../models/demand_forecast.pkl')
FEATURE_COLUMNS_PATH = os.path.join(BASE_DIR, '../../models/feature_columns.pkl')
DATA_PATH = os.path.join(BASE_DIR, '../../data/cleaned_data.csv')
