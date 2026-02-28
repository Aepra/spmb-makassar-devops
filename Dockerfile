# 1. Gunakan image Python yang ringan
FROM python:3.9-slim

# 2. Set folder kerja di dalam kontainer
WORKDIR /app

# 3. Copy file requirements dulu (agar build lebih cepat)
COPY requirements.txt .

# 4. Install library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy seluruh kode aplikasi kita ke dalam kontainer
COPY . .

# 6. Perintah untuk menjalankan FastAPI
# Kita pakai host 0.0.0.0 agar bisa diakses dari luar kontainer
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]