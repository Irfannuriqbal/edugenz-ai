# 🎓 EduGenZ AI - Intelligent Learning Platform

> Platform pembelajaran cerdas yang menggabungkan kekuatan AI untuk membantu siswa memahami materi dengan lebih efektif.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Fitur Utama

### 📚 Manajemen Materi

- Upload file PDF dengan mudah
- Tampilkan daftar materi dengan informasi lengkap
- Hapus materi yang tidak diperlukan

### 📖 Ringkasan Otomatis

- Generate ringkasan materi menggunakan AI Gemini
- Lihat ringkasan dengan tampilan profesional
- Copy atau download ringkasan sebagai file TXT
- Cetak ringkasan langsung
- Kelola daftar ringkasan yang telah dibuat

### 🎯 Quiz Interaktif

- Generate quiz otomatis dari materi PDF
- Interface quiz modern dengan progress bar
- Tampilkan hasil dengan badge grading (A/B/C/D)
- Review jawaban dengan feedback detail
- Kelola daftar quiz dan hasil ujian

### 💬 AI Chatbot

- Tanya jawab dengan AI Gemini tentang materi
- Interface chat modern dengan bubble messaging
- Timestamp dan avatar untuk setiap pesan
- Auto-scroll untuk kenyamanan pengguna

### 📊 Dashboard Terpadu

- Statistik sistem (Total Materi, Ringkasan, Quiz, Rata-rata Nilai)
- Timeline aktivitas terbaru
- Quick action buttons untuk akses cepat
- Responsive design untuk semua ukuran layar

### 📱 Responsive Design

- Optimasi untuk mobile, tablet, dan desktop
- Bootstrap 5 dengan custom theme #2563eb
- Modern UI dengan card shadows dan rounded corners

## 🚀 Instalasi

### Prasyarat

- Python 3.12 atau lebih tinggi
- pip (Python package manager)
- Google Generative AI API Key (dapatkan dari [Google AI Studio](https://ai.google.dev/))

### Langkah 1: Clone Repository

```bash
git clone https://github.com/yourusername/edugenz-ai.git
cd edugenz-ai
```

### Langkah 2: Setup Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Langkah 4: Konfigurasi Environment

```bash
# Copy file contoh environment
cp .env.example .env

# Edit .env dan isi dengan nilai Anda
# Terutama: GEMINI_API_KEY dan SECRET_KEY
```

### Langkah 5: Jalankan Aplikasi

```bash
# Menggunakan run.py
python run.py

# Atau menggunakan Flask CLI
flask run

# Atau menggunakan Gunicorn (production)
gunicorn --bind 0.0.0.0:5000 backend.app:app
```

Aplikasi akan berjalan di `http://localhost:5000`

## 🐳 Instalasi dengan Docker

### Prasyarat

- Docker Desktop terinstall
- Docker Compose (biasanya sudah termasuk di Docker Desktop)

### Langkah 1: Siapkan Environment

```bash
cp .env.example .env
# Edit .env dengan nilai Anda
```

### Langkah 2: Build & Run dengan Docker Compose

```bash
# Build image
docker build -f docker/Dockerfile -t edugenz-ai .

# Jalankan dengan docker-compose
cd docker
docker-compose up -d

# Atau jalankan container secara langsung
docker run -d \
  --name edugenz-ai \
  -p 5000:5000 \
  -v uploads_data:/app/frontend/static/uploads \
  -v db_data:/app/backend/database \
  -e GEMINI_API_KEY=your-key \
  -e SECRET_KEY=your-secret \
  edugenz-ai
```

Aplikasi akan berjalan di `http://localhost:5000`

### Membantu Docker Compose

```bash
# Lihat status container
docker-compose ps

# Lihat logs
docker-compose logs -f

# Stop container
docker-compose down

# Stop dan remove volume
docker-compose down -v
```

## ☁️ Deployment ke Cloud

### Azure Container Instances (ACI)

```bash
# Login ke Azure
az login

# Create resource group
az group create --name edugenz-rg --location eastus

# Create container
az container create \
  --resource-group edugenz-rg \
  --name edugenz-ai \
  --image edugenz-ai:latest \
  --ports 5000 \
  --environment-variables GEMINI_API_KEY=your-key SECRET_KEY=your-secret
```

### Azure App Service

```bash
# Create App Service plan
az appservice plan create --name edugenz-plan --resource-group edugenz-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group edugenz-rg --plan edugenz-plan --name edugenz-ai --runtime "PYTHON:3.12"

# Deploy aplikasi
az webapp deployment source config-zip --resource-group edugenz-rg --name edugenz-ai --src deploy.zip
```

### Docker Hub

```bash
# Login ke Docker Hub
docker login

# Tag image
docker tag edugenz-ai:latest yourusername/edugenz-ai:latest

# Push ke Docker Hub
docker push yourusername/edugenz-ai:latest

# Deploy di platform lain yang support Docker Hub
```

## 📖 Penggunaan

### Dashboard

1. Buka aplikasi di `http://localhost:5000`
2. Lihat statistik sistem dan aktivitas terbaru
3. Gunakan quick action buttons untuk navigasi cepat

### Upload PDF

1. Klik "📤 Upload PDF" atau navigasi ke menu Upload
2. Drag & drop file PDF atau klik untuk memilih
3. File akan tersimpan dan siap digunakan

### Generate Ringkasan

1. Klik "✨ Generate Ringkasan" atau navigasi ke menu Ringkasan
2. Pilih file materi dari dropdown
3. Klik "Generate" dan tunggu proses AI
4. Lihat ringkasan, copy, download, atau cetak

### Generate Quiz

1. Klik "🎯 Generate Quiz" atau navigasi ke menu Quiz
2. Pilih file materi dari dropdown
3. Klik "Generate" dan tunggu proses AI
4. Mulai quiz dan jawab semua pertanyaan
5. Lihat hasil dengan badge grading

### Chat dengan AI

1. Navigasi ke menu "💬 Chatbot"
2. Ketik pertanyaan tentang materi
3. AI akan menjawab dalam sebuah percakapan
4. Scroll otomatis untuk melihat pesan terbaru

## 📁 Struktur Direktori

```
edugenz-ai/
├── backend/
│   ├── app.py              # Flask app initialization & dashboard
│   ├── config.py           # Configuration settings
│   ├── utils.py            # Database utilities
│   ├── routes/
│   │   ├── upload_routes.py     # Upload management
│   │   ├── summary_routes.py    # Summary generation
│   │   ├── chatbot_routes.py    # Chatbot interface
│   │   └── quiz_routes.py       # Quiz management
│   ├── services/
│   │   ├── gemini_service.py    # AI integration
│   │   └── quiz_service.py      # Quiz logic
│   └── database/
│       └── edugenz.db           # SQLite database
├── frontend/
│   ├── templates/
│   │   ├── base.html            # Master template
│   │   ├── dashboard.html       # Home page
│   │   ├── upload.html          # File upload
│   │   ├── summary.html         # Summary generator
│   │   ├── summary_list.html    # Summary history
│   │   ├── summary_detail.html  # View summary
│   │   ├── quiz.html            # Quiz generator
│   │   ├── quiz_list.html       # Quiz history
│   │   ├── quiz_attempt.html    # Quiz interface
│   │   ├── quiz_result.html     # Quiz results
│   │   └── chatbot.html         # Chatbot interface
│   └── static/
│       ├── css/
│       │   └── style.css        # Custom styling
│       ├── js/
│       │   └── main.js          # JavaScript utilities
│       └── uploads/             # User uploaded files
├── docker/
│   ├── Dockerfile               # Production Dockerfile
│   └── docker-compose.yml       # Docker Compose config
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .dockerignore                # Docker ignore rules
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🔧 Konfigurasi

### Environment Variables

Lihat `.env.example` untuk daftar lengkap. Yang paling penting:

| Variable         | Deskripsi                      | Contoh                          |
| ---------------- | ------------------------------ | ------------------------------- |
| `GEMINI_API_KEY` | Google Generative AI API Key   | `AIzaSy...`                     |
| `SECRET_KEY`     | Flask secret key untuk session | `your-secret-key`               |
| `FLASK_ENV`      | Environment mode               | `production` atau `development` |
| `DATABASE_URL`   | Database connection string     | `sqlite:///edugenz.db`          |

### Database Schema

Aplikasi menggunakan SQLite dengan tabel:

- `uploads` - File PDF yang diupload
- `summaries` - Ringkasan yang dihasilkan
- `quizzes` - Quiz yang dihasilkan
- `quiz_attempts` - Hasil attempt quiz
- `chats` - History percakapan chatbot

## 🐛 Troubleshooting

### Port sudah digunakan

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

### GEMINI_API_KEY tidak valid

1. Pastikan key benar di file `.env`
2. Cek di [Google AI Studio](https://ai.google.dev/)
3. Generate key baru jika perlu

### Error database

```bash
# Reset database
rm backend/database/edugenz.db
python -c "from backend.app import init_db; init_db()"
```

### Docker error pada Windows

Pastikan WSL 2 terinstall dan Docker Desktop menggunakan WSL 2 backend.

## 📚 Dependencies

- **Flask 3.1.3** - Web framework
- **python-dotenv 1.0.0** - Environment management
- **google-generativeai 0.8.6** - Google Gemini API
- **pypdf 6.13.0** - PDF text extraction
- **Werkzeug 3.1.2** - WSGI utilities
- **Gunicorn 22.0.0** - Production server

## 🎨 Design System

- **Primary Color**: #2563eb (Blue)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)
- **Neutral**: Gray scale

## 🤝 Kontribusi

Kami menerima kontribusi! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Lisensi

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👤 Author

**Irfan Nur Iqbal**

- KOMPUTASI AWAN - UAS Final Project
- Universitas Indonesia

## 🙏 Terima Kasih

Terima kasih kepada:

- Google untuk API Generative AI
- Flask team untuk web framework
- Bootstrap untuk UI framework
- Semua library open source yang digunakan

## 📞 Support

Untuk dukungan, email ke:

- 📧 contact@edugenz.ai
- 📧 irfan.nur.iqbal@example.com

Atau buka issue di GitHub repository.

---

**Happy Learning! 🚀**

_Platform ini dibuat untuk membantu siswa belajar lebih efektif dengan bantuan AI modern._
