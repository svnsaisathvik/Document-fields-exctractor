import os
from datetime import timedelta

class Config:
    """Base configuration"""
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
    
    # Flask settings
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True
    
    # Tesseract path (adjust based on your OS)
    TESSERACT_PATH = r'/usr/bin/tesseract'  # Linux path

class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True

class ProductionConfig(Config):
    """Production config"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}