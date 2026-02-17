from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from backend.config import Config
from backend.models import db, Admin, Event, Happening, Glimpse

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

def convert_youtube_url_to_embed(url):
    """
    Convert any YouTube URL format to embed format
    Handles: youtu.be, youtube.com/watch, m.youtube.com/watch, etc.
    """
    if not url:
        return url
    
    # Already in embed format
    if 'youtube.com/embed/' in url:
        return url
    
    import re
    
    # Extract video ID from different formats
    video_id = None
    
    # Format: https://youtu.be/VIDEO_ID
    if 'youtu.be/' in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
    
    # Format: https://www.youtube.com/watch?v=VIDEO_ID or https://youtube.com/watch?v=VIDEO_ID
    elif 'youtube.com/watch' in url or 'm.youtube.com/watch' in url:
        match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
    
    # If we found a video ID, return embed URL
    if video_id:
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Return original if we couldn't parse it
    return url

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

# Add new event
@app.route('/api/admin/events', methods=['POST'])
def add_event():
    try:
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        
        # Validate required fields
        if not all([title, description, event_date]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Handle file upload
        if 'image' not in request.files:
            return jsonify({'error': 'Image is required'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            unique_filename = f"{timestamp}_{filename}"
            
            # Save to static/images folder
            static_images_path = os.path.join('static', 'images', unique_filename)
            os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
            file.save(static_images_path)
            
            # Also save to frontend/public/images for development
            frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
            os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
            file.seek(0)  # Reset file pointer
            file.save(frontend_images_path)
            
            # Create event in database
            event = Event(
                title=title,
                description=description,
                event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
                image_path=f"images/{unique_filename}"
            )
            db.session.add(event)
            db.session.commit()
            
            return jsonify({'message': 'Event added successfully', 'event': event.to_dict()}), 201
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Add new happening
@app.route('/api/admin/happenings', methods=['POST'])
def add_happening():
    try:
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Validate required fields
        if not all([title, description]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Handle file upload
        if 'image' not in request.files:
            return jsonify({'error': 'Image is required'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            unique_filename = f"{timestamp}_{filename}"
            
            # Save to static/images folder
            static_images_path = os.path.join('static', 'images', unique_filename)
            os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
            file.save(static_images_path)
            
            # Also save to frontend/public/images for development
            frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
            os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
            file.seek(0)  # Reset file pointer
            file.save(frontend_images_path)
            
            # Create happening in database
            happening = Happening(
                title=title,
                description=description,
                image_path=f"images/{unique_filename}"
            )
            db.session.add(happening)
            db.session.commit()
            
            return jsonify({'message': 'Happening added successfully', 'happening': happening.to_dict()}), 201
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete event
@app.route('/api/admin/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        # Delete image file if it exists
        if event.image_path:
            # Delete from static/images
            static_file_path = os.path.join('static', event.image_path)
            if os.path.exists(static_file_path):
                os.remove(static_file_path)
            
            # Delete from frontend/public/images
            frontend_file_path = os.path.join('frontend', 'public', event.image_path)
            if os.path.exists(frontend_file_path):
                os.remove(frontend_file_path)
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete happening
@app.route('/api/admin/happenings/<int:happening_id>', methods=['DELETE'])
def delete_happening(happening_id):
    try:
        happening = Happening.query.get(happening_id)
        if not happening:
            return jsonify({'error': 'Happening not found'}), 404
        
        # Delete image file if it exists
        if happening.image_path:
            # Delete from static/images
            static_file_path = os.path.join('static', happening.image_path)
            if os.path.exists(static_file_path):
                os.remove(static_file_path)
            
            # Delete from frontend/public/images
            frontend_file_path = os.path.join('frontend', 'public', happening.image_path)
            if os.path.exists(frontend_file_path):
                os.remove(frontend_file_path)
        
        db.session.delete(happening)
        db.session.commit()
        
        return jsonify({'message': 'Happening deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get single event by ID
@app.route('/api/admin/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        return jsonify(event.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update event
@app.route('/api/admin/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        
        # Update fields
        if title:
            event.title = title
        if description:
            event.description = description
        if event_date:
            event.event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
        
        # Handle image upload if new image provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image
                if event.image_path:
                    # Delete from static/images
                    old_static_path = os.path.join('static', event.image_path)
                    if os.path.exists(old_static_path):
                        os.remove(old_static_path)
                    
                    # Delete from frontend/public/images
                    old_frontend_path = os.path.join('frontend', 'public', event.image_path)
                    if os.path.exists(old_frontend_path):
                        os.remove(old_frontend_path)
                
                # Save new image
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                # Save to static/images
                static_images_path = os.path.join('static', 'images', unique_filename)
                os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
                file.save(static_images_path)
                
                # Save to frontend/public/images
                frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
                os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
                file.seek(0)
                file.save(frontend_images_path)
                
                event.image_path = f"images/{unique_filename}"
        
        db.session.commit()
        return jsonify({'message': 'Event updated successfully', 'event': event.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get single happening by ID
@app.route('/api/admin/happenings/<int:happening_id>', methods=['GET'])
def get_happening(happening_id):
    try:
        happening = Happening.query.get(happening_id)
        if not happening:
            return jsonify({'error': 'Happening not found'}), 404
        return jsonify(happening.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update happening
@app.route('/api/admin/happenings/<int:happening_id>', methods=['PUT'])
def update_happening(happening_id):
    try:
        happening = Happening.query.get(happening_id)
        if not happening:
            return jsonify({'error': 'Happening not found'}), 404
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Update fields
        if title:
            happening.title = title
        if description:
            happening.description = description
        
        # Handle image upload if new image provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image
                if happening.image_path:
                    # Delete from static/images
                    old_static_path = os.path.join('static', happening.image_path)
                    if os.path.exists(old_static_path):
                        os.remove(old_static_path)
                    
                    # Delete from frontend/public/images
                    old_frontend_path = os.path.join('frontend', 'public', happening.image_path)
                    if os.path.exists(old_frontend_path):
                        os.remove(old_frontend_path)
                
                # Save new image
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                # Save to static/images
                static_images_path = os.path.join('static', 'images', unique_filename)
                os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
                file.save(static_images_path)
                
                # Save to frontend/public/images
                frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
                os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
                file.seek(0)
                file.save(frontend_images_path)
                
                happening.image_path = f"images/{unique_filename}"
        
        db.session.commit()
        return jsonify({'message': 'Happening updated successfully', 'happening': happening.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= GLIMPSES API =============

# Get all glimpses
@app.route('/api/glimpses', methods=['GET'])
def get_glimpses():
    try:
        glimpses = Glimpse.query.filter_by(is_active=True).order_by(Glimpse.created_at.desc()).all()
        return jsonify([glimpse.to_dict() for glimpse in glimpses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add new glimpse
@app.route('/api/admin/glimpses', methods=['POST'])
def add_glimpse():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        hashtags = request.form.get('hashtags', '')
        
        if not all([title, description, video_url]):
            return jsonify({'error': 'Title, description, and video URL are required'}), 400
        
        if 'image' not in request.files:
            return jsonify({'error': 'Image is required'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            unique_filename = f"{timestamp}_{filename}"
            
            static_images_path = os.path.join('static', 'images', unique_filename)
            os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
            file.save(static_images_path)
            
            frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
            os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
            file.seek(0)
            file.save(frontend_images_path)
            
            glimpse = Glimpse(
                title=title,
                description=description,
                image_path=f"images/{unique_filename}",
                video_url=video_url,
                hashtags=hashtags
            )
            db.session.add(glimpse)
            db.session.commit()
            
            return jsonify({'message': 'Glimpse added successfully', 'glimpse': glimpse.to_dict()}), 201
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete glimpse
@app.route('/api/admin/glimpses/<int:glimpse_id>', methods=['DELETE'])
def delete_glimpse(glimpse_id):
    try:
        glimpse = Glimpse.query.get(glimpse_id)
        if not glimpse:
            return jsonify({'error': 'Glimpse not found'}), 404
        
        if glimpse.image_path:
            static_file_path = os.path.join('static', glimpse.image_path)
            if os.path.exists(static_file_path):
                os.remove(static_file_path)
            
            frontend_file_path = os.path.join('frontend', 'public', glimpse.image_path)
            if os.path.exists(frontend_file_path):
                os.remove(frontend_file_path)
        
        db.session.delete(glimpse)
        db.session.commit()
        
        return jsonify({'message': 'Glimpse deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get single glimpse by ID
@app.route('/api/admin/glimpses/<int:glimpse_id>', methods=['GET'])
def get_glimpse(glimpse_id):
    try:
        glimpse = Glimpse.query.get(glimpse_id)
        if not glimpse:
            return jsonify({'error': 'Glimpse not found'}), 404
        return jsonify(glimpse.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update glimpse
@app.route('/api/admin/glimpses/<int:glimpse_id>', methods=['PUT'])
def update_glimpse(glimpse_id):
    try:
        glimpse = Glimpse.query.get(glimpse_id)
        if not glimpse:
            return jsonify({'error': 'Glimpse not found'}), 404
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        hashtags = request.form.get('hashtags', '')
        
        # Update fields
        if title:
            glimpse.title = title
        if description:
            glimpse.description = description
        if video_url:
            # Convert YouTube URL to embed format automatically
            glimpse.video_url = convert_youtube_url_to_embed(video_url)
        if hashtags is not None:  # Allow empty string
            glimpse.hashtags = hashtags
        
        # Handle image upload if new image provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image
                if glimpse.image_path:
                    old_static_path = os.path.join('static', glimpse.image_path)
                    if os.path.exists(old_static_path):
                        os.remove(old_static_path)
                    
                    old_frontend_path = os.path.join('frontend', 'public', glimpse.image_path)
                    if os.path.exists(old_frontend_path):
                        os.remove(old_frontend_path)
                
                # Save new image
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                static_images_path = os.path.join('static', 'images', unique_filename)
                os.makedirs(os.path.dirname(static_images_path), exist_ok=True)
                file.save(static_images_path)
                
                frontend_images_path = os.path.join('frontend', 'public', 'images', unique_filename)
                os.makedirs(os.path.dirname(frontend_images_path), exist_ok=True)
                file.seek(0)
                file.save(frontend_images_path)
                
                glimpse.image_path = f"images/{unique_filename}"
        
        db.session.commit()
        return jsonify({'message': 'Glimpse updated successfully', 'glimpse': glimpse.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

# Serve React static files (only if build folder exists - for local development)
# On Railway, frontend is served by Vercel, so this won't be used
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # Check if static folder exists (it won't on Railway)
    if not os.path.exists(app.static_folder):
        return jsonify({
            'message': 'Backend API is running',
            'status': 'ok',
            'endpoints': {
                'health': '/api/health',
                'events': '/api/events',
                'happenings': '/api/happenings',
                'glimpses': '/api/glimpses'
            }
        }), 200
    
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({
                'message': 'Backend API is running',
                'status': 'ok',
                'note': 'Frontend is served separately on Vercel'
            }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port)
