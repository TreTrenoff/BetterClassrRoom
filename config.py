"""
Configuration file for BetterClassRoom application
"""

# Database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///betterclassroom.db"

# App settings
DEBUG = True
SECRET_KEY = "your-secret-key-here"
PORT = 5000
HOST = "localhost"

# Login configuration
LOG_LEVEL = "INFO"
LOG_FILE = "betterclassroom.log"

# Other settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
TIMEOUT = 30