# Builder stage
FROM python:3.12-slim AS builder
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY . /app

# Install cron and tzdata
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

# Create folders for cron logs and data
RUN mkdir -p /cron /data && chmod 755 /cron /data

# Setup cron
RUN crontab cron/2fa-cron

# Decrypt seed before starting services
RUN python3 decrypt.py

# Start both cron and FastAPI
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8080"]
