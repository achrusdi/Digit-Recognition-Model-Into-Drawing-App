# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
# import os

load_dotenv()  # Muat variabel dari file .env

def create_app():
    app = Flask(__name__)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
