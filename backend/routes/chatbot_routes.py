from datetime import datetime
from flask import Blueprint, render_template, request, flash
from backend.utils import get_db_connection
from backend.services.gemini_service import ask_chatbot

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    response = None
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            flash("Silakan masukkan pertanyaan terlebih dahulu.", "danger")
        else:
            try:
                answer = ask_chatbot(question)
                response = {
                    "question": question,
                    "answer": answer,
                }
                conn = get_db_connection()
                conn.execute(
                    "INSERT INTO chats (question, answer, asked_at) VALUES (?, ?, ?)",
                    (question, answer, datetime.utcnow().isoformat()),
                )
                conn.commit()
                conn.close()
                flash("Jawaban chatbot berhasil dibuat.", "success")
            except Exception as exc:
                flash(str(exc), "danger")

    return render_template("chatbot.html", response=response)
