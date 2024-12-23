import os

class Config:
    """Base configuration with common settings for all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")  # Secret key for session management and CSRF protection
    DEBUG = False  # Default to False, specific environments will override this
    TESTING = False  # Default to False, for testing purposes only
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking for SQLAlchemy (to save resources)
    
    # Database configuration (assuming you might use SQLAlchemy in the future)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///calendar.db")  # Default to SQLite database

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True  # Enable debug mode for development
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///dev_calendar.db")  # Dev database

class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True  # Enable testing mode
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///test_calendar.db")  # Test database

class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False  # Disable debug mode in production
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL", "sqlite:///prod_calendar.db")  # Production database

# Create a dictionary to easily access the configuration by environment
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
