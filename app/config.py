from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# Ensure data directory exists
data_dir = Path("data")
data_dir.mkdir(exist_ok=True) 