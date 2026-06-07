import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-env")
    UPLOAD_FOLDER = str(BASE_DIR.parent / "frontend" / "static" / "uploads")
    DATABASE_PATH = str(BASE_DIR / "database" / "app.db")
