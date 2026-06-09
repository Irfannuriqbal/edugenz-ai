# API Documentation - EduGenZ AI

## Base URL

Production:

https://edugenz-ai.myvnc.com

## Authentication

Saat ini API digunakan secara internal oleh aplikasi EduGenZ AI.

---

## Upload Learning Material

### Endpoint

POST /upload

### Description

Mengunggah file PDF pembelajaran ke sistem dan menyimpannya pada Cloudflare R2 Storage.

### Request

Content-Type:

multipart/form-data

Parameter:

| Parameter | Type | Description          |
| --------- | ---- | -------------------- |
| file      | PDF  | Dokumen pembelajaran |

### Response

```json
{
  "status": "success",
  "message": "File uploaded successfully"
}
```

---

## Analyze Document

### Endpoint

POST /analyze

### Description

Menganalisis isi dokumen menggunakan Google Gemini AI.

### Response

```json
{
  "summary": "...",
  "topics": [...]
}
```

---

## Generate Quiz

### Endpoint

POST /quiz

### Description

Menghasilkan kuis otomatis berdasarkan materi yang telah dianalisis.

### Response

```json
{
  "questions": [
    {
      "question": "...",
      "options": [...],
      "answer": "..."
    }
  ]
}
```

---

## Generate Recommendation

### Endpoint

POST /recommendation

### Description

Memberikan rekomendasi pembelajaran berdasarkan hasil analisis AI.

### Response

```json
{
  "recommendation": "..."
}
```

---

## Storage Service

Cloudflare R2 digunakan sebagai object storage untuk menyimpan dokumen PDF pengguna.

## Artificial Intelligence Service

Google Gemini API digunakan untuk:

* Content Analysis
* Quiz Generation
* Learning Recommendation
* Educational Assistance

* API Key Gemini disimpan menggunakan environment variables.
* Kredensial tidak disimpan pada repository publik.
* Komunikasi dilakukan menggunakan HTTPS.
