@echo off
REM Deployment script for DFA Minimizer Web Application (Windows)

echo 🚀 Deploying DFA Minimizer Web Application
echo ==========================================

REM Set environment variables for production
set FLASK_ENV=production
set FLASK_DEBUG=false

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run tests
echo 🧪 Running tests...
python run_tests.py
if %errorlevel% neq 0 (
    echo ❌ Tests failed! Deployment aborted.
    exit /b 1
)

REM Start the application
echo 🎉 Starting application...
echo Application will be available at http://localhost:5000
echo Press Ctrl+C to stop the server

python app.py
