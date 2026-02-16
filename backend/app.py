from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from models import db, Admin, Event, Happening

# Initialize Flask API application
# Set static folder to serve React build
app = Flask(__name__, 
            static_folder='../frontend/build',
            static_url_path='')
app.config.from_object(Config)

# Session configuration for CORS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Enable CORS for React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://*.vercel.app", "https://*.railway.app", "https://*.up.railway.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize extensions
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ============= API ROUTES =============

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200

# Get all events
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = Event.query.filter_by(is_active=True).order_by(Event.event_date).all()
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all happenings
@app.route('/api/happenings', methods=['GET'])
def get_happenings():
    try:
        happenings = Happening.query.filter_by(is_active=True).order_by(Happening.created_at.desc()).all()
        return jsonify([happening.to_dict() for happening in happenings]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Contact form
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not all([name, email, message]):
            return jsonify({'error': 'All fields are required'}), 400
        
        msg = Message('Contact Form Submission',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)
        
        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to send message'}), 500

# Admin login
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return jsonify({'message': 'Login successful', 'user': {'username': admin.username}}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin logout
@app.route('/api/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Get current admin user
@app.route('/api/admin/me', methods=['GET'])
@login_required
def get_current_admin():
    return jsonify({'username': current_user.username}), 200

# Database initialization
try:
    with app.app_context():
        db.create_all()
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created')
except Exception as e:
    print(f'Database initialization: {e}')

# ============= SERVE REACT APP =============

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port)
