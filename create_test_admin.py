#!/usr/bin/env python
"""Script to create a test admin user for the admin dashboard"""

from app import app, db
from models import Admin

def create_test_admin():
    """Create a test admin user"""
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
        
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user 'admin' already exists!")
            return
        
        # Create new admin user
        admin = Admin()
        admin.username = 'admin'
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Test admin user created successfully!")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nYou can now log in to the admin dashboard at /admin/login")

if __name__ == '__main__':
    create_test_admin()
