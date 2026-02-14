# Flask College Website

A simple Flask-based college website with contact form functionality.

## Setup

1. Create virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure email in `app.py`:
   - Update `MAIL_USERNAME` and `MAIL_PASSWORD`

4. Run the application:
   ```
   python app.py
   ```

5. Visit `http://localhost:5000`

## Structure

- `app.py` - Main application file
- `templates/` - HTML templates
- `static/css/` - CSS stylesheets
- `requirements.txt` - Python dependencies
