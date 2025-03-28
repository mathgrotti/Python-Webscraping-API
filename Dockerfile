FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install beautifulsoup4 requests pdfplumber pandas

VOLUME /app/data