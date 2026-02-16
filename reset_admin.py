import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app, db, Admin

def reset_admin():
    with app.app_context():
        # Delete existing admin
        Admin.query.delete()
        db.session.commit()
        print("Deleted existing admin users")
        
        # Create new admin
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        
        # Verify
        test_admin = Admin.query.filter_by(username='admin').first()
        if test_admin:
            print(f"\n✓ Verification: Admin user exists in database (ID: {test_admin.id})")
            # Test password
            if test_admin.check_password('admin123'):
                print("✓ Password verification: SUCCESS")
            else:
                print("✗ Password verification: FAILED")
        else:
            print("\n✗ Verification: Admin user NOT found in database")

if __name__ == '__main__':
    reset_admin()
