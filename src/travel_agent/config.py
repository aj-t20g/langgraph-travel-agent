"""Configuration management for the travel agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for the travel agent."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    # LLM Settings
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    DEFAULT_TEMPERATURE = 0.7

    # Validation
    @classmethod
    def validate(cls) -> list[str]:
        """Validate that required environment variables are set.

        Returns:
            List of missing configuration keys
        """
        missing = []

        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")

        if not cls.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")

        return missing

    @classmethod
    def is_valid(cls) -> bool:
        """Check if configuration is valid.

        Returns:
            True if all required keys are set
        """
        return len(cls.validate()) == 0


# Validate configuration on import
_missing_keys = Config.validate()
if _missing_keys:
    print(f"Warning: Missing environment variables: {', '.join(_missing_keys)}")
    print("Please create a .env file with the required keys. See .env.example for reference.")
