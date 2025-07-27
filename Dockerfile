FROM python:3.10-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install system dependencies for pdfplumber and OCR
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libtiff5-dev \
        libopenjp2-7 \
        libglib2.0-0 \
        tesseract-ocr \
        tesseract-ocr-all \
        poppler-utils \
        ghostscript \
        libmagic1 \
        fonts-noto-core \
        fonts-noto-cjk \
        fonts-noto-color-emoji \
        fonts-noto-extra \
        fonts-noto-ui-core \
        fonts-noto-ui-extra \
        fonts-noto-unhinted && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

CMD ["python", "process_pdfs.py"]
