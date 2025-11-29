# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install python deps
RUN pip install --no-cache-dir -r ../requirements.txt || pip install --no-cache-dir flask flask-cors

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
