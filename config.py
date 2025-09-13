"""
Configuration settings for DFA Minimizer Web Application
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Application settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # File upload settings (for future DFA file upload feature)
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # DFA processing limits
    MAX_STATES = 100  # Maximum number of states allowed
    MAX_ALPHABET_SIZE = 20  # Maximum alphabet size
    MAX_INPUT_STRING_LENGTH = 1000  # Maximum input string length for simulation
    
    # Example DFA settings
    EXAMPLES_FOLDER = os.path.join(os.path.dirname(__file__), 'examples')
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE', 'False').lower() == 'true'
    LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-change-me'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    
# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
