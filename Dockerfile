FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY traineddata /usr/share/tesseract-ocr/5/tessdata

COPY . .

EXPOSE 50100

CMD ["python", "app.py"]
