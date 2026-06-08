import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from werkzeug.utils import secure_filename
from backend.services.gemini_service import extract_text_from_pdf
from backend.utils import get_db_connection, allowed_file

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("pdf_file")
        if not file or file.filename == "":
            flash("Pilih file PDF terlebih dahulu.", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Format tidak valid. Hanya PDF yang diizinkan.", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        try:
            extracted_text = extract_text_from_pdf(save_path)
            if not extracted_text:
                flash("PDF berhasil diunggah, tetapi teks tidak dapat diekstrak.", "warning")
            else:
                flash("PDF berhasil diunggah dan teks berhasil diekstrak.", "success")
        except Exception as exc:
            flash(f"PDF berhasil diunggah, tetapi terjadi kesalahan saat ekstraksi: {exc}", "warning")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO uploads (filename, uploaded_at) VALUES (?, ?)",
            (filename, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("upload.upload"))

    conn = get_db_connection()
    uploads = conn.execute("SELECT * FROM uploads ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return render_template("upload.html", uploads=uploads)


@upload_bp.route("/view-pdf/<filename>")
def view_pdf(filename):
    """View PDF file in browser"""
    filename = secure_filename(filename)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    
    if not os.path.exists(file_path):
        flash("File tidak ditemukan.", "danger")
        return redirect(url_for("upload.upload"))
    
    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=filename
    )


@upload_bp.route("/delete/<filename>", methods=["POST"])
def delete_upload(filename):
    """Delete uploaded file"""
    filename = secure_filename(filename)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    
    # Delete file if exists
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as exc:
            flash(f"Gagal menghapus file: {str(exc)}", "danger")
            return redirect(url_for("upload.upload"))
    
    # Delete from database
    conn = get_db_connection()
    conn.execute("DELETE FROM uploads WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()
    
    flash(f"File {filename} berhasil dihapus.", "success")
    return redirect(url_for("upload.upload"))
