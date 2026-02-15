@echo off
echo ========================================
echo  Haridwar University Admin Panel Setup
echo ========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in PATH
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✓ .env file created
    echo.
    echo IMPORTANT: Edit .env file and add your email credentials!
    echo.
) else (
    echo ✓ .env file already exists
    echo.
)

echo [5/5] Initializing database...
flask init-db
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo ✓ Database initialized
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Default Admin Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Next Steps:
echo   1. Edit .env file with your email settings
echo   2. Run: python app.py
echo   3. Visit: http://localhost:5000/admin/login
echo.
echo Press any key to start the application...
pause >nul

python app.py
