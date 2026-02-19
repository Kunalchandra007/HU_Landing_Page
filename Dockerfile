FROM python:3.13-slim

WORKDIR /app

# Install PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
    libpq5 \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files from backend
COPY backend/app.py backend/api.py backend/models.py backend/config.py backend/wsgi.py ./
COPY backend/static ./static

# Create instance directory
RUN mkdir -p instance

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD gunicorn app:app --bind 0.0.0.0:$PORT
