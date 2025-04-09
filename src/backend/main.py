from flask import Flask
from src.backend.routes.prediction_routes import prediction_bp

app = Flask(__name__)

# Register the blueprint with a URL prefix
app.register_blueprint(prediction_bp, url_prefix="/predict")

# Optional: Root route for quick check
@app.route("/")
def home():
    return "Flask app is running. Visit /predict/predict"

# Function to print registered routes
def print_registered_routes():
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

# Run the app
if __name__ == "__main__":
    print_registered_routes()  # Print routes on startup
    app.run(debug=True)
