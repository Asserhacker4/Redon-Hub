FROM python:3.11-slim

WORKDIR /app

# تثبيت أدوات النظام المطلوبة
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# تثبيت مكتبات بايثون الأصلية بالكامل
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع
COPY . .

# توليد ملفات Prisma
RUN python3 -m prisma generate

# ضبط بورت Hugging Face البيئي وتحديد مسار بايثون
ENV PYTHONPATH=.
EXPOSE 7860

# تشغيل البوت عبر ملف launcher
CMD ["python3", "-u", "redonhub/launcher.py"]
