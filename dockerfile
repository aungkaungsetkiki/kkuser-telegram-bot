# Build stage
FROM python:3.9 as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Final stage
FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-mya
COPY . .
CMD ["python", "bot.py"]
