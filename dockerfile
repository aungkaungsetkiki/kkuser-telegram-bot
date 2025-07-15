FROM python:3.10-slim-buster

# System dependencies များတပ်ဆင်ခြင်း
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-mya \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Working directory သတ်မှတ်ခြင်း
WORKDIR /app

# Requirements တပ်ဆင်ခြင်း
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code ကူးယူခြင်း
COPY . .

# Bot ကို run မည့် command
CMD ["python", "bot.py"]
