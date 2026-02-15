from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy database instance
# This will be configured in app.py with the database URI from config.py
db = SQLAlchemy()

# Admin Model - Stores admin user credentials for dashboard access
class Admin(UserMixin, db.Model):
    """
    Admin user model for authentication and authorization
    Table: admin
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password for security
    
    def set_password(self, password):
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

# Event Model - Stores upcoming university events
class Event(db.Model):
    """
    Event model for managing university events
    Table: event
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(200), nullable=False)  # Event title
    description = db.Column(db.Text, nullable=False)  # Event description
    event_date = db.Column(db.Date, nullable=False)  # Date of the event
    image_path = db.Column(db.String(300), nullable=False)  # Path to event image
    is_active = db.Column(db.Boolean, default=True)  # Toggle event visibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update timestamp
    
    def to_dict(self):
        """Convert event object to dictionary for JSON responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date.strftime('%Y-%m-%d'),
            'image_path': self.image_path,
            'is_active': self.is_active
        }

# Happening Model - Stores recent happenings/news at the university
class Happening(db.Model):
    """
    Happening model for managing university news and recent activities
    Table: happening
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(200), nullable=False)  # Happening title
    description = db.Column(db.Text, nullable=False)  # Happening description
    image_path = db.Column(db.String(300), nullable=False)  # Path to happening image
    is_active = db.Column(db.Boolean, default=True)  # Toggle happening visibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update timestamp
    
    def to_dict(self):
        """Convert happening object to dictionary for JSON responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_path': self.image_path,
            'is_active': self.is_active
        }
