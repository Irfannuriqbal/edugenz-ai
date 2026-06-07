import logging
import os
from pathlib import Path

import google.generativeai as genai
from pypdf import PdfReader


def _configure_gemini() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY tidak ditemukan. Tambahkan ke file .env atau environment variables.")
    genai.configure(api_key=api_key)


def _truncate_text(text: str, max_length: int = 15000) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n\n[TEKS TERPUTUS, SILAKAN GUNAKAN MATERI YANG LEBIH SINGKAT]"


def _generate_from_gemini(prompt: str) -> str:
    _configure_gemini()
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=1024,
            ),
        )
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "Maaf, Gemini tidak mengembalikan jawaban yang dapat dibaca."
    except Exception as exc:
        logging.exception("Gemini request failed")
        raise RuntimeError("Terjadi kesalahan saat memanggil Gemini API. Silakan cek konfigurasi API key dan coba lagi.") from exc


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    if not pages:
        return ""
    full_text = "\n\n".join(pages).strip()
    return _truncate_text(full_text)


def ask_chatbot(question: str) -> str:
    question = question.strip()
    if not question:
        return "Silakan ajukan pertanyaan terlebih dahulu."
    prompt = (
        "Anda adalah asisten edukasi yang membantu mahasiswa menjawab pertanyaan dengan jelas, singkat, "
        "dan sesuai konteks pembelajaran. Jawab pertanyaan berikut: \n\n"
        f"{question}"
    )
    return _generate_from_gemini(prompt)


def generate_summary(text: str) -> str:
    text = text.strip()
    if not text:
        return "Tidak ada teks yang dapat diringkas."
    prompt = (
        "Ringkas materi berikut secara DETAIL menjadi poin-poin penting dan penjelasan untuk mahasiswa. "
        "Sertakan penjelasan mendalam untuk setiap poin penting:\n\n"
        f"{text}"
    )
    _configure_gemini()
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "Maaf, Gemini tidak mengembalikan jawaban yang dapat dibaca."
    except Exception as exc:
        logging.exception("Gemini request failed")
        raise RuntimeError("Terjadi kesalahan saat memanggil Gemini API. Silakan cek konfigurasi API key dan coba lagi.") from exc


def generate_quiz(text: str) -> str:
    text = text.strip()
    if not text:
        return "Tidak ada teks yang dapat diubah menjadi quiz."
    prompt = (
        "Buat 10 soal pilihan ganda dari materi berikut. Gunakan format TEPAT ini untuk setiap soal:\n\n"
        "Soal 1: [Pertanyaan di sini?]\n"
        "A) Pilihan A\n"
        "B) Pilihan B\n"
        "C) Pilihan C\n"
        "D) Pilihan D\n"
        "Jawaban: X\n\n"
        "Soal 2: ... dan seterusnya\n\n"
        "MATERI:\n"
        f"{text}"
    )
    _configure_gemini()
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "Maaf, Gemini tidak mengembalikan jawaban yang dapat dibaca."
    except Exception as exc:
        logging.exception("Gemini request failed")
        raise RuntimeError("Terjadi kesalahan saat memanggil Gemini API. Silakan cek konfigurasi API key dan coba lagi.") from exc
