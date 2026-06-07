import sqlite3
from pathlib import Path
from flask import current_app


def get_db_connection(app=None):
    config = app.config if app is not None else current_app.config
    db_path = config["DATABASE_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


def ensure_directories(app):
    uploads_path = Path(app.config["UPLOAD_FOLDER"])
    db_path = Path(app.config["DATABASE_PATH"])
    uploads_path.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)
