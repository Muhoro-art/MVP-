# src/backend/main.py

import os
from flask import Flask
from .routes.inventory_routes import inventory_bp
from src.backend.routes.prediction_routes import prediction_bp

def create_app():
    app = Flask(__name__)


    # Register Blueprints
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(prediction_bp, url_prefix='/predict')

    return app

if __name__ == '__main__':
    app = create_app()
    # Debug mode is fine for MVP, but be cautious for production
    app.run(debug=True, host='127.0.0.1', port=5000)
