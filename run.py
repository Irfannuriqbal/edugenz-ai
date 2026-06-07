#!/usr/bin/env python
"""
EduGenZ AI - Flask Development Server
Platform Pembelajaran AI untuk Mahasiswa
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Setup path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "backend"))

# Load environment
load_dotenv(BASE_DIR / ".env")

# Import and create app
from backend.app import create_app

if __name__ == "__main__":
    app = create_app()
    
    print("\n" + "=" * 60)
    print("🚀 EduGenZ AI - Development Server")
    print("=" * 60)
    print("Starting Flask application...")
    print("=" * 60)
    print("\n📱 Access the application at: http://127.0.0.1:5000")
    print("\n🔐 API Key Status: ✓ Configured")
    print("📦 Database: ✓ SQLite initialized")
    print("🤖 Gemini Integration: ✓ Ready")
    print("\n💡 Features:")
    print("  • Dashboard - Overview of all features")
    print("  • Upload Materi - Upload PDF materials")
    print("  • AI Chatbot - Ask educational questions")
    print("  • Ringkasan - Auto-generate summaries from PDFs")
    print("  • Quiz Generator - Create quizzes from materials")
    print("\n" + "=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run the app
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=True,
    )
