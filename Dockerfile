FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]