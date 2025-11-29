"""
Configuration settings for the KB-Agent backend
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""
    
    # Flask settings
    DEBUG = os.getenv('FLASK_DEBUG', True)
    TESTING = os.getenv('TESTING', False)
    
    # Server settings
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///kb_agent.db')
    
    # Vector DB settings
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './chroma_db')
    
    # Embedding model settings
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # API settings
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    MAX_RESULTS = int(os.getenv('MAX_RESULTS', 10))
    MIN_SIMILARITY_SCORE = float(os.getenv('MIN_SIMILARITY_SCORE', 0.3))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/kb_agent.log')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', True)
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', True)
    
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    
    # Document settings
    MAX_DOCUMENT_SIZE = int(os.getenv('MAX_DOCUMENT_SIZE', 10 * 1024 * 1024))  # 10MB
    ALLOWED_DOCUMENT_TYPES = ['pdf', 'txt', 'docx', 'md']
    
    # Search settings
    SEARCH_TOP_K = int(os.getenv('SEARCH_TOP_K', 3))
    SEARCH_THRESHOLD = float(os.getenv('SEARCH_THRESHOLD', 0.5))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    VECTOR_DB_PATH = './test_chroma_db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
