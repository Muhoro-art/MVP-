import joblib
import os

MODEL_PATH = os.path.join("models", "demand_forecast.pkl")

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        raise Exception("Model not found. Please ensure demand_forecast.pkl exists in the models directory.")

def predict_inventory(day):
    if day <= 0:
        raise ValueError("Day must be a positive integer.")
    
    model = load_model()
    prediction = model.predict([[day]])  # Assuming model expects [[day]]
    return round(prediction[0], 2)
