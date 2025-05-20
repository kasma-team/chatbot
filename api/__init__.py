from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    # Load environment variables
    load_dotenv()
    
    # Register API routes
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app