import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production-12345')
    
    # Database configuration with SSL support for Supabase/PostgreSQL
    # Gets DATABASE_URL from environment variables, defaults to in-memory SQLite
    database_url = os.getenv('DATABASE_URL')
    
    # If no DATABASE_URL is set, use persistent SQLite database file
    if not database_url:
        # Use instance folder for database file
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'university.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    elif database_url.startswith('postgresql'):
        # Add SSL mode for PostgreSQL connections (required by Supabase and most cloud providers)
        if '?' in database_url:
            # If URL already has query parameters, append with &
            SQLALCHEMY_DATABASE_URI = database_url + '&sslmode=require'
        else:
            # If no query parameters, add with ?
            SQLALCHEMY_DATABASE_URI = database_url + '?sslmode=require'
    else:
        # Use database URL as-is for SQLite or other databases
        SQLALCHEMY_DATABASE_URI = database_url
    
    # Disable SQLAlchemy modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration for Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif'}
