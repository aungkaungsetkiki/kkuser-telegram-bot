FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-mya \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "bot.py"]
