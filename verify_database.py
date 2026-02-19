#!/usr/bin/env python3
"""
Script to verify database connection and check data persistence
Run this to test if PostgreSQL is properly configured
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app, db
from backend.models import Admin, Event, Happening, Glimpse

def verify_database():
    """Verify database connection and show current data"""
    with app.app_context():
        try:
            # Check database type
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'postgresql' in db_uri:
                print("✅ Using PostgreSQL (persistent storage)")
                print(f"   Connection: {db_uri.split('@')[1] if '@' in db_uri else 'localhost'}")
            elif 'sqlite' in db_uri:
                print("⚠️  Using SQLite (ephemeral on Railway!)")
                print(f"   Database file: {db_uri.replace('sqlite:///', '')}")
            else:
                print(f"❓ Unknown database type: {db_uri}")
            
            print("\n" + "="*60)
            
            # Check admin users
            admins = Admin.query.all()
            print(f"\n👤 Admin Users: {len(admins)}")
            for admin in admins:
                print(f"   - {admin.username}")
            
            # Check events
            events = Event.query.all()
            print(f"\n📅 Events: {len(events)}")
            for event in events:
                status = "✓ Active" if event.is_active else "✗ Inactive"
                print(f"   - {event.title} ({status})")
            
            # Check happenings
            happenings = Happening.query.all()
            print(f"\n📰 Happenings: {len(happenings)}")
            for happening in happenings:
                status = "✓ Active" if happening.is_active else "✗ Inactive"
                print(f"   - {happening.title} ({status})")
            
            # Check glimpses
            glimpses = Glimpse.query.all()
            print(f"\n🎬 Glimpses: {len(glimpses)}")
            for glimpse in glimpses:
                status = "✓ Active" if glimpse.is_active else "✗ Inactive"
                has_image = "🖼️" if glimpse.image_path else "📹"
                print(f"   {has_image} {glimpse.title} ({status})")
            
            print("\n" + "="*60)
            print("\n✅ Database connection successful!")
            
            if 'sqlite' in db_uri and 'railway' in os.environ.get('RAILWAY_ENVIRONMENT', '').lower():
                print("\n⚠️  WARNING: You're using SQLite on Railway!")
                print("   Data will be lost on every redeploy.")
                print("   Please add PostgreSQL database to your Railway project.")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Database error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("="*60)
    print("DATABASE VERIFICATION")
    print("="*60)
    verify_database()
