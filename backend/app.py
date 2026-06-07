import sqlite3
from pathlib import Path
from flask import Flask, render_template, url_for, jsonify
from config import Config
from utils import ensure_directories, get_db_connection
from routes.upload_routes import upload_bp
from routes.chatbot_routes import chatbot_bp
from routes.summary_routes import summary_bp
from routes.quiz_routes import quiz_bp

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app():
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "frontend" / "templates"),
        static_folder=str(BASE_DIR / "frontend" / "static"),
    )
    app.config.from_object(Config)
    app.secret_key = app.config.get("SECRET_KEY", "dev-secret-key")
    ensure_directories(app)
    register_blueprints(app)
    init_db(app)
    return app


def register_blueprints(app):
    app.register_blueprint(upload_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(quiz_bp)


def init_db(app):
    conn = get_db_connection(app)
    
    # Create tables
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            uploaded_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            summary TEXT NOT NULL,
            title TEXT,
            generated_at TEXT NOT NULL
        )
        """
    )
    
    # Add title column if it doesn't exist (migration)
    try:
        conn.execute("ALTER TABLE summaries ADD COLUMN title TEXT")
    except:
        pass  # Column already exists
    
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            quiz TEXT NOT NULL,
            title TEXT,
            generated_at TEXT NOT NULL
        )
        """
    )
    
    # Add title column to quizzes if it doesn't exist (migration)
    try:
        conn.execute("ALTER TABLE quizzes ADD COLUMN title TEXT")
    except:
        pass  # Column already exists
    
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            answers TEXT NOT NULL,
            score REAL,
            total_questions INTEGER,
            attempted_at TEXT NOT NULL,
            FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            asked_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


app = create_app()


@app.route("/")
@app.route("/dashboard")
def dashboard():
    conn = get_db_connection(app)
    total_materi = conn.execute("SELECT COUNT(*) FROM uploads").fetchone()[0]
    total_summary = conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0]
    total_quiz = conn.execute("SELECT COUNT(*) FROM quizzes").fetchone()[0]
    total_chat = conn.execute("SELECT COUNT(*) FROM chats").fetchone()[0]
    
    # Hitung rata-rata nilai quiz
    avg_score_result = conn.execute("SELECT AVG(score) FROM quiz_attempts").fetchone()
    avg_score = avg_score_result[0] if avg_score_result[0] is not None else 0
    
    # Ambil aktivitas terbaru (gabungan dari uploads, summaries, quizzes, quiz_attempts)
    recent_activities = []
    
    # Recent uploads
    uploads = conn.execute(
        "SELECT 'Upload', filename, uploaded_at FROM uploads ORDER BY uploaded_at DESC LIMIT 5"
    ).fetchall()
    for activity in uploads:
        recent_activities.append({
            'type': 'Upload',
            'description': f"Upload: {activity[1]}",
            'timestamp': activity[2]
        })
    
    # Recent summaries
    summaries = conn.execute(
        "SELECT 'Summary', title, generated_at FROM summaries ORDER BY generated_at DESC LIMIT 5"
    ).fetchall()
    for activity in summaries:
        recent_activities.append({
            'type': 'Summary',
            'description': f"Ringkasan: {activity[1]}",
            'timestamp': activity[2]
        })
    
    # Recent quiz attempts
    attempts = conn.execute(
        "SELECT 'Quiz', quizzes.title, quiz_attempts.attempted_at, quiz_attempts.score FROM quiz_attempts JOIN quizzes ON quiz_attempts.quiz_id = quizzes.id ORDER BY quiz_attempts.attempted_at DESC LIMIT 5"
    ).fetchall()
    for activity in attempts:
        recent_activities.append({
            'type': 'Quiz',
            'description': f"Quiz: {activity[1]} ({activity[3]:.0f}%)",
            'timestamp': activity[2]
        })
    
    # Sort by timestamp descending
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = recent_activities[:10]  # Take top 10
    
    conn.close()

    quick_actions = [
        {"label": "📤 Upload PDF", "url": url_for("upload.upload")},
        {"label": "💬 Buka Chatbot", "url": url_for("chatbot.chatbot")},
        {"label": "📖 Buat Ringkasan", "url": url_for("summary.generate")},
        {"label": "🎯 Buat Quiz", "url": url_for("quiz.generate")},
    ]

    return render_template(
        "dashboard.html",
        total_materi=total_materi,
        total_summary=total_summary,
        total_quiz=total_quiz,
        total_chat=total_chat,
        avg_score=round(avg_score, 1),
        recent_activities=recent_activities,
        quick_actions=quick_actions,
    )


@app.route("/api/stats")
def stats():
    """API endpoint untuk get stats"""
    conn = get_db_connection(app)
    total_materi = conn.execute("SELECT COUNT(*) FROM uploads").fetchone()[0]
    total_summary = conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0]
    total_quiz = conn.execute("SELECT COUNT(*) FROM quizzes").fetchone()[0]
    total_attempts = conn.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0]
    
    avg_score_result = conn.execute("SELECT AVG(score) FROM quiz_attempts").fetchone()
    avg_score = round(avg_score_result[0], 1) if avg_score_result[0] is not None else 0
    
    conn.close()
    
    return jsonify({
        'total_materi': total_materi,
        'total_summary': total_summary,
        'total_quiz': total_quiz,
        'total_attempts': total_attempts,
        'avg_score': avg_score
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
