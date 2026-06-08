import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
from backend.utils import get_db_connection
from backend.services.gemini_service import extract_text_from_pdf, generate_summary

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/summary", methods=["GET"])
def summary():
    """List semua ringkasan yang sudah dibuat"""
    conn = get_db_connection()
    summaries = conn.execute(
        "SELECT id, filename, title, generated_at FROM summaries ORDER BY generated_at DESC"
    ).fetchall()
    conn.close()
    return render_template("summary_list.html", summaries=summaries)


@summary_bp.route("/summary/<int:summary_id>", methods=["GET"])
def summary_detail(summary_id):
    """Detail satu ringkasan"""
    conn = get_db_connection()
    summary = conn.execute(
        "SELECT id, filename, title, summary, generated_at FROM summaries WHERE id = ?",
        (summary_id,),
    ).fetchone()
    conn.close()

    if not summary:
        flash("Ringkasan tidak ditemukan.", "danger")
        return render_template("summary_list.html", summaries=[])

    return render_template("summary_detail.html", summary=summary)


@summary_bp.route("/summary/generate", methods=["GET", "POST"])
def generate():
    """Generate ringkasan baru"""
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
                    summary_text = generate_summary(text)
                    title = selected_file.rsplit(".", 1)[0]  # Hapus .pdf dari filename
                    conn.execute(
                        "INSERT INTO summaries (filename, title, summary, generated_at) VALUES (?, ?, ?, ?)",
                        (selected_file, title, summary_text, datetime.utcnow().isoformat()),
                    )
                    conn.commit()
                    flash("Ringkasan berhasil dibuat.", "success")
                    # Redirect ke halaman list
                    return render_template("summary_list.html", summaries=conn.execute(
                        "SELECT id, filename, title, generated_at FROM summaries ORDER BY generated_at DESC"
                    ).fetchall())
            except Exception as exc:
                flash(str(exc), "danger")

    conn.close()
    return render_template("summary_generate.html", uploads=uploads)


@summary_bp.route("/summary/<int:summary_id>/delete", methods=["POST"])
def delete_summary(summary_id):
    """Delete ringkasan"""
    conn = get_db_connection()
    conn.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))
    conn.commit()
    conn.close()
    
    flash("Ringkasan berhasil dihapus.", "success")
    return redirect(url_for("summary.summary"))
