from flask import Flask
from config import Config
from extensions import bcrypt, cors
from api.urls import register_routes
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True, resources={
        r"/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    logging.getLogger('pymongo').setLevel(logging.WARNING)
    register_routes(app)
    return app