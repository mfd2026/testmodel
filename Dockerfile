# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    HF_HOME=/app/hf_cache

# حزم خفيفة (لو احتجت شهادات/SSL فقط)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) ثبّت المتطلبات أولاً (طبقة مستقلة لتحسين الكاش)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2) انسخ الكود
COPY app ./app

# 3) انسخ الأوزان (مهم: بعد التثبيت)
COPY weights ./weights

# مستخدم غير-root
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
