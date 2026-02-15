from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from models import db, Admin, Event, Happening

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Public Routes
@app.route('/')
def home():
    events = Event.query.filter_by(is_active=True).order_by(Event.event_date).all()
    happenings = Happening.query.filter_by(is_active=True).order_by(Happening.created_at.desc()).all()
    return render_template('index.html', events=events, happenings=happenings)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        try:
            msg = Message('Contact Form Submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash('Failed to send message. Please try again.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Admin Authentication Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

# Admin Dashboard Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/dashboard.html', events=events)

@app.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
def admin_add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date = datetime.strptime(request.form.get('event_date'), '%Y-%m-%d').date()
        
        # Handle file upload
        if 'image' not in request.files:
            flash('No image file provided', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Store relative path for database
            image_path = f"uploads/events/{filename}"
            
            event = Event(
                title=title,
                description=description,
                event_date=event_date,
                image_path=image_path
            )
            db.session.add(event)
            db.session.commit()
            
            flash('Event added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file type. Allowed types: png, jpg, jpeg, gif, webp, avif', 'error')
    
    return render_template('admin/add_event.html')

@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.event_date = datetime.strptime(request.form.get('event_date'), '%Y-%m-%d').date()
        
        # Handle file upload if new image provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and file and allowed_file(file.filename):
                # Delete old image
                old_image_path = os.path.join('static', event.image_path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                event.image_path = f"uploads/events/{filename}"
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/events/delete/<int:event_id>', methods=['POST'])
@login_required
def admin_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Delete image file
    image_path = os.path.join('static', event.image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/events/toggle/<int:event_id>', methods=['POST'])
@login_required
def admin_toggle_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.is_active = not event.is_active
    db.session.commit()
    
    status = 'activated' if event.is_active else 'deactivated'
    return jsonify({'success': True, 'message': f'Event {status}', 'is_active': event.is_active})

# Happenings Management Routes
@app.route('/admin/happenings')
@login_required
def admin_happenings():
    happenings = Happening.query.order_by(Happening.created_at.desc()).all()
    return render_template('admin/happenings.html', happenings=happenings)

@app.route('/admin/happenings/add', methods=['GET', 'POST'])
@login_required
def admin_add_happening():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Handle file upload
        if 'image' not in request.files:
            flash('No image file provided', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Store relative path for database
            image_path = f"uploads/events/{filename}"
            
            happening = Happening(
                title=title,
                description=description,
                image_path=image_path
            )
            db.session.add(happening)
            db.session.commit()
            
            flash('Happening added successfully!', 'success')
            return redirect(url_for('admin_happenings'))
        else:
            flash('Invalid file type. Allowed types: png, jpg, jpeg, gif, webp, avif', 'error')
    
    return render_template('admin/add_happening.html')

@app.route('/admin/happenings/edit/<int:happening_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_happening(happening_id):
    happening = Happening.query.get_or_404(happening_id)
    
    if request.method == 'POST':
        happening.title = request.form.get('title')
        happening.description = request.form.get('description')
        
        # Handle file upload if new image provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and file and allowed_file(file.filename):
                # Delete old image
                old_image_path = os.path.join('static', happening.image_path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                happening.image_path = f"uploads/events/{filename}"
        
        db.session.commit()
        flash('Happening updated successfully!', 'success')
        return redirect(url_for('admin_happenings'))
    
    return render_template('admin/edit_happening.html', happening=happening)

@app.route('/admin/happenings/delete/<int:happening_id>', methods=['POST'])
@login_required
def admin_delete_happening(happening_id):
    happening = Happening.query.get_or_404(happening_id)
    
    # Delete image file
    image_path = os.path.join('static', happening.image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    db.session.delete(happening)
    db.session.commit()
    
    flash('Happening deleted successfully!', 'success')
    return redirect(url_for('admin_happenings'))

@app.route('/admin/happenings/toggle/<int:happening_id>', methods=['POST'])
@login_required
def admin_toggle_happening(happening_id):
    happening = Happening.query.get_or_404(happening_id)
    happening.is_active = not happening.is_active
    db.session.commit()
    
    status = 'activated' if happening.is_active else 'deactivated'
    return jsonify({'success': True, 'message': f'Happening {status}', 'is_active': happening.is_active})

# Initialize database and create admin user
@app.cli.command()
def init_db():
    """Initialize the database and create admin user."""
    db.create_all()
    
    # Check if admin exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('admin123')  # Change this password!
        db.session.add(admin)
        db.session.commit()
        print('Database initialized! Admin user created (username: admin, password: admin123)')
    else:
        print('Database already initialized!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
