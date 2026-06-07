#!/usr/bin/env python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env from project root
root = Path(__file__).resolve().parent
load_dotenv(root / ".env")

print("=" * 60)
print("VERIFICATION CHECKLIST")
print("=" * 60)

# 1. Python version
print(f"✓ Python version: {sys.version.split()[0]}")

# 2. Check .env
api_key = os.environ.get("GEMINI_API_KEY")
print(f"✓ GEMINI_API_KEY loaded: {bool(api_key)}")
if api_key:
    print(f"  Key (masked): {api_key[:10]}...{api_key[-5:]}")

# 3. Check required packages
required_packages = {
    'flask': 'Flask',
    'google.generativeai': 'google-generativeai',
    'pypdf': 'pypdf',
    'dotenv': 'python-dotenv',
}

print("\n✓ Installed packages:")
for module, package_name in required_packages.items():
    try:
        __import__(module)
        print(f"  - {package_name}: OK")
    except ImportError:
        print(f"  - {package_name}: MISSING")

# 4. Check directories
base_dir = root / "backend"
dirs_to_check = [
    (base_dir / "database", "Database folder"),
    (root / "frontend" / "static" / "uploads", "Uploads folder"),
    (root / "frontend" / "templates", "Templates folder"),
    (base_dir / "routes", "Routes folder"),
    (base_dir / "services", "Services folder"),
]

print("\n✓ Project structure:")
for dir_path, label in dirs_to_check:
    exists = dir_path.exists()
    status = "OK" if exists else "MISSING"
    print(f"  - {label}: {status}")

# 5. Check critical files
files_to_check = [
    (base_dir / "app.py", "app.py"),
    (base_dir / "config.py", "config.py"),
    (base_dir / "utils.py", "utils.py"),
    (base_dir / "services" / "gemini_service.py", "gemini_service.py"),
    (base_dir / "routes" / "chatbot_routes.py", "chatbot_routes.py"),
    (root / ".env", ".env"),
]

print("\n✓ Critical files:")
for file_path, label in files_to_check:
    exists = file_path.exists()
    status = "OK" if exists else "MISSING"
    print(f"  - {label}: {status}")

print("\n" + "=" * 60)
print("All checks completed!")
print("=" * 60)
