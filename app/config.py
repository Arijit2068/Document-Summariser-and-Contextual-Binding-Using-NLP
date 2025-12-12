"""
Configuration settings for the Document Summarizer application
"""

import os
from pathlib import Path

class Config:
    """Base configuration"""
    
    # Application settings
    DEBUG = False
    TESTING = False
    
    # Model settings
    MODEL_NAME = "t5-base"  # Fallback model name
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.safetensors')
    TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), '..')
    
    # Max input/output lengths
    MAX_INPUT_LENGTH = 512
    MAX_OUTPUT_LENGTH = 200
    MIN_OUTPUT_LENGTH = 30
    
    # Summarization parameters
    NUM_BEAMS = 4
    NO_REPEAT_NGRAM_SIZE = 3
    LENGTH_PENALTY = 2.0
    EARLY_STOPPING = True
    
    # Device settings
    DEVICE = "cpu"  # Change to "cuda" if GPU is available
    
    # History settings
    HISTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'history.json')
    
    # Flask settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
