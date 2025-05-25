import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Config
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
PROJECT_NAME = os.getenv("PROJECT_NAME", "Personalized Education API")

# Database Config
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Construct DATABASE_URL if not present but individual credentials are available
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if all([DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME]):
        DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
    else:
        raise ValueError("Either DATABASE_URL or all database credentials must be set in .env file")

# Mistral AI Config
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    print("Warning: MISTRAL_API_KEY environment variable is not set in .env file")

# Default Mistral model to use
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

# Beyond Presence API Config
BEY_API_KEY = os.getenv("BEY_API_KEY")
if not BEY_API_KEY:
    print("Warning: BEY_API_KEY environment variable is not set in .env file")