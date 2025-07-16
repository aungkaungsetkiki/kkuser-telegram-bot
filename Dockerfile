FROM python:3.10-slim-bullseye

# Tesseract OCR နှင့် Burmese language ထည့်သွင်းခြင်း
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-mya \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
