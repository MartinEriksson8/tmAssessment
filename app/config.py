from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta
import secrets

# Load environment variables from .env file
load_dotenv()

# Database configuration
# Default to SQLite, but support PostgreSQL if DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# Ensure data directory exists for SQLite
if DATABASE_URL.startswith("sqlite"):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

# JWT Configuration
# Generate a secure random key if not set in environment
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

