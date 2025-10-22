import logging
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_FILENAME: str
    LOG_LEVEL: str = "INFO"

    @property
    def database_url(self) -> str:
        return f"sqlite:///./{self.DB_FILENAME}"

# Configure logging based on LOG_LEVEL from environment
def setup_logging(log_level: str):
    # Convert string level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure basic logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Create settings instance
settings = Settings(_env_file='.env') # type: ignore

# Setup logging with the configured level
setup_logging(settings.LOG_LEVEL)