# AI Documentation - EduGenZ AI

## Overview

EduGenZ AI adalah platform pembelajaran cerdas yang memanfaatkan Large Language Model (LLM) Google Gemini untuk membantu siswa memahami materi pembelajaran secara lebih efektif melalui analisis dokumen, pembuatan kuis otomatis, dan rekomendasi pembelajaran.

## Artificial Intelligence Technology

### AI Provider

Google Gemini API

### AI Model Function

Model AI digunakan untuk:

1. Menganalisis isi dokumen pembelajaran yang diunggah pengguna.
2. Menghasilkan ringkasan materi secara otomatis.
3. Membuat soal kuis berdasarkan materi yang dipelajari.
4. Memberikan rekomendasi pembelajaran yang sesuai dengan konteks materi.

## Workflow

### Document Analysis

1. Pengguna mengunggah dokumen PDF.
2. Sistem mengekstrak teks dari dokumen.
3. Teks dikirim ke Google Gemini API.
4. Gemini melakukan analisis terhadap konten.
5. Hasil analisis ditampilkan kepada pengguna.

### Quiz Generation

1. Materi pembelajaran diproses oleh AI.
2. Gemini menghasilkan pertanyaan berdasarkan isi materi.
3. Sistem menampilkan kuis kepada pengguna.
4. Pengguna dapat menggunakan kuis sebagai evaluasi pembelajaran.

### Learning Recommendation

1. AI mengidentifikasi topik utama dalam materi.
2. Sistem menghasilkan rekomendasi pembelajaran lanjutan.
3. Rekomendasi diberikan untuk meningkatkan pemahaman pengguna.

## Input

* PDF Learning Material
* Extracted Text Content
* User Learning Request

## Output

* Material Summary
* AI Generated Quiz
* Learning Recommendation
* Topic Analysis

## Advantages

* Otomatisasi pembuatan materi evaluasi.
* Membantu siswa memahami materi lebih cepat.
* Mengurangi waktu pembuatan soal secara manual.
* Mendukung pembelajaran berbasis Artificial Intelligence.

## Security

* API Key Gemini disimpan menggunakan environment variables.
* Kredensial tidak disimpan pada repository publik.
* Komunikasi dilakukan menggunakan HTTPS.
