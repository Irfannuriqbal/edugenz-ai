import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from backend.utils import get_db_connection
from backend.services.gemini_service import extract_text_from_pdf, generate_quiz
from backend.services.quiz_service import parse_quiz_text, generate_random_correct_answers, calculate_score, get_question_result, get_badge_grade

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/quiz", methods=["GET"])
def quiz():
    """List semua quiz yang tersedia"""
    conn = get_db_connection()
    quizzes = conn.execute(
        "SELECT id, filename, title, generated_at FROM quizzes ORDER BY generated_at DESC"
    ).fetchall()
    conn.close()
    return render_template("quiz_list.html", quizzes=quizzes)


@quiz_bp.route("/quiz/generate", methods=["GET", "POST"])
def generate():
    """Generate quiz baru"""
    conn = get_db_connection()
    uploads = conn.execute("SELECT filename FROM uploads ORDER BY uploaded_at DESC").fetchall()

    if request.method == "POST":
        selected_file = request.form.get("filename")
        if not selected_file:
            flash("Pilih materi terlebih dahulu.", "danger")
        else:
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], selected_file)
            try:
                text = extract_text_from_pdf(file_path)
                if not text:
                    flash("Tidak ada teks yang dapat diekstrak dari file PDF.", "danger")
                else:
                    quiz_text = generate_quiz(text)
                    # Parse quiz text -> questions JSON
                    questions = parse_quiz_text(quiz_text)
                    questions = generate_random_correct_answers(questions)
                    
                    title = selected_file.rsplit(".", 1)[0]
                    conn.execute(
                        "INSERT INTO quizzes (filename, title, quiz, generated_at) VALUES (?, ?, ?, ?)",
                        (selected_file, title, json.dumps(questions), datetime.utcnow().isoformat()),
                    )
                    conn.commit()
                    flash("Quiz berhasil dibuat!", "success")
                    return render_template("quiz_list.html", quizzes=conn.execute(
                        "SELECT id, filename, title, generated_at FROM quizzes ORDER BY generated_at DESC"
                    ).fetchall())
            except Exception as exc:
                flash(f"Error: {str(exc)}", "danger")

    conn.close()
    return render_template("quiz_generate.html", uploads=uploads)


@quiz_bp.route("/quiz/<int:quiz_id>/attempt", methods=["GET"])
def attempt(quiz_id):
    """Halaman untuk mengerjakan quiz"""
    conn = get_db_connection()
    quiz = conn.execute(
        "SELECT id, filename, title, quiz FROM quizzes WHERE id = ?",
        (quiz_id,),
    ).fetchone()
    conn.close()

    if not quiz:
        flash("Quiz tidak ditemukan.", "danger")
        return redirect(url_for("quiz.quiz"))

    try:
        # Try to parse as JSON first (new format)
        questions = json.loads(quiz['quiz'])
        # Validate it's a list of questions
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError("Invalid format")
    except:
        # Old format - parse from text
        questions = parse_quiz_text(quiz['quiz'])
        questions = generate_random_correct_answers(questions)

    return render_template("quiz_attempt.html", quiz=quiz, questions=questions, total=len(questions))


@quiz_bp.route("/quiz/<int:quiz_id>/submit", methods=["POST"])
def submit(quiz_id):
    """Submit jawaban quiz"""
    conn = get_db_connection()
    quiz = conn.execute(
        "SELECT id, filename, title, quiz FROM quizzes WHERE id = ?",
        (quiz_id,),
    ).fetchone()
    conn.close()

    if not quiz:
        flash("Quiz tidak ditemukan.", "danger")
        return redirect(url_for("quiz.quiz"))

    try:
        questions = json.loads(quiz['quiz'])
        answers = {}
        
        # Collect answers dari form
        for i in range(len(questions)):
            answer = request.form.get(f"answer_{i}")
            if answer:
                answers[str(i)] = answer
        
        # Calculate score
        result = calculate_score(questions, answers)
        
        # Save attempt ke database
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO quiz_attempts (quiz_id, answers, score, total_questions, attempted_at) VALUES (?, ?, ?, ?, ?)",
            (quiz_id, json.dumps(answers), result['percentage'], len(questions), datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
        
        # Store result di session untuk tampilkan di halaman result
        session[f'quiz_result_{quiz_id}'] = {
            'quiz_id': quiz_id,
            'title': quiz['title'],
            'answers': answers,
            'score': result
        }
        
        return redirect(url_for('quiz.result', quiz_id=quiz_id))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("quiz.quiz"))


@quiz_bp.route("/quiz/<int:quiz_id>/result", methods=["GET"])
def result(quiz_id):
    """Tampilkan hasil dan review jawaban"""
    conn = get_db_connection()
    quiz = conn.execute(
        "SELECT id, filename, title, quiz FROM quizzes WHERE id = ?",
        (quiz_id,),
    ).fetchone()
    conn.close()

    if not quiz:
        flash("Quiz tidak ditemukan.", "danger")
        return redirect(url_for("quiz.quiz"))

    quiz_result = session.get(f'quiz_result_{quiz_id}')
    if not quiz_result:
        flash("Hasil quiz tidak ditemukan. Silakan erjakan quiz terlebih dahulu.", "info")
        return redirect(url_for("quiz.attempt", quiz_id=quiz_id))

    try:
        questions = json.loads(quiz['quiz'])
        answers = quiz_result['answers']
        score = quiz_result['score']
        
        # Get badge grade
        badge = get_badge_grade(score['percentage'])
        
        # Generate result details untuk setiap soal
        question_results = []
        for idx, question in enumerate(questions):
            user_answer = answers.get(str(idx))
            if user_answer:
                qr = get_question_result(question, user_answer, idx)
                question_results.append(qr)
        
        return render_template(
            "quiz_result.html",
            quiz_title=quiz['title'],
            quiz_id=quiz_id,
            score=score,
            badge=badge,
            question_results=question_results
        )
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("quiz.quiz"))


@quiz_bp.route("/quiz/<int:quiz_id>/delete", methods=["POST"])
def delete_quiz(quiz_id):
    """Delete quiz dan semua attempt-nya"""
    conn = get_db_connection()
    conn.execute("DELETE FROM quiz_attempts WHERE quiz_id = ?", (quiz_id,))
    conn.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
    conn.commit()
    conn.close()
    
    flash("Quiz berhasil dihapus.", "success")
    return redirect(url_for("quiz.quiz"))
