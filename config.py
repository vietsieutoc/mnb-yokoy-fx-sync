"""
Configuration module for MNB Yokoy FX Sync

Loads configuration from environment variables and .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings"""
    
    # Yokoy API settings
    YOKOY_API_URL = os.getenv('YOKOY_API_URL', 'https://app.yokoy.io/public/v1')
    YOKOY_API_KEY = os.getenv('YOKOY_API_KEY')
    
    # Debug mode
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.YOKOY_API_KEY:
            errors.append("YOKOY_API_KEY is not set")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def is_configured(cls):
        """Check if Yokoy integration is configured"""
        return cls.YOKOY_API_KEY is not None
