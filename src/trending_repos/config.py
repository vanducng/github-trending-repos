"""Configuration management for the application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Email settings
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    RECIPIENT_EMAIL: str = os.getenv("RECIPIENT_EMAIL", "me@vanducng.dev")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "GitHub Trending <onboarding@resend.dev>")
    
    # GitHub settings
    GITHUB_TOKEN: Optional[str] = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    
    # Trending settings
    TRENDING_PERIOD: str = os.getenv("TRENDING_PERIOD", "daily")  # daily, weekly, monthly
    TRENDING_LANGUAGE: str = os.getenv("TRENDING_LANGUAGE", "")  # empty for all languages
    
    @classmethod
    def validate_required_settings(cls) -> bool:
        """Validate that all required settings are provided.
        
        Returns:
            True if all required settings are available, False otherwise
        """
        required_settings = [
            ("RESEND_API_KEY", cls.RESEND_API_KEY),
            ("RECIPIENT_EMAIL", cls.RECIPIENT_EMAIL),
        ]
        
        missing_settings = []
        for setting_name, setting_value in required_settings:
            if not setting_value:
                missing_settings.append(setting_name)
        
        if missing_settings:
            print(f"Missing required environment variables: {', '.join(missing_settings)}")
            print("Please set these in your environment or .env file")
            return False
        
        return True