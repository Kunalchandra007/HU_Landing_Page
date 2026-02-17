FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ backend/

# Copy static and other necessary files
COPY static/ static/

# Create instance directory for database
RUN mkdir -p backend/instance

# Expose port
EXPOSE 8080

# Start command - use exec form with bash
CMD ["bash", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8080} backend.app:app"]
