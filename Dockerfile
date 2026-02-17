FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy all files
COPY . .

# Create instance directory for database
RUN mkdir -p backend/instance

# Set environment variable for Python path
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Use Python to run gunicorn with PORT from environment
ENTRYPOINT ["python", "-c", "import os; import subprocess; port = os.environ.get('PORT', '8080'); subprocess.run(['gunicorn', '-w', '4', '-b', f'0.0.0.0:{port}', 'backend.app:app'])"]
