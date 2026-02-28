FROM python:3.10-slim

WORKDIR /app

# Install dependencies sistem untuk PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Jalankan FastAPI di port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]