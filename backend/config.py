import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List, Dict


class Settings(BaseSettings):
    """Application settings"""
    google_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"


def load_config():
    """Load configuration from plan file"""
    config_path = Path(__file__).parent.parent / "plan"

    # Parse the plan file to extract YAML config
    with open(config_path, 'r') as f:
        content = f.read()

    # Extract YAML portion (starts after line 7)
    lines = content.split('\n')
    yaml_start = 7  # After the initial description
    yaml_content = '\n'.join(lines[yaml_start:])

    config = yaml.safe_load(yaml_content)
    return config


# Load settings
settings = Settings()
config = load_config()

# Extract configuration sections
SOURCES = config.get('sources', [])
LLM_CONFIG = config.get('llm', {})
KEYWORDS = config.get('keywords', {})
DISPLAY_CONFIG = config.get('display', {})
