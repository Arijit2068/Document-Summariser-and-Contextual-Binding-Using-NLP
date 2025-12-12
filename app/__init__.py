"""
Document Summarizer and Contextual Binding using NLP
Main application package initialization
"""

from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='../ui/templates',
                static_folder='../ui/static')
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    from app.config import Config
    app.config.from_object(Config)
    
    return app
