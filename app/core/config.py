import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Config
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
PROJECT_NAME = os.getenv("PROJECT_NAME", "Personalized Education API")

# Database Config
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set in .env file")