#!/bin/bash
# Deployment script for DFA Minimizer Web Application

echo "🚀 Deploying DFA Minimizer Web Application"
echo "=========================================="

# Set environment variables for production
export FLASK_ENV=production
export FLASK_DEBUG=false

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python run_tests.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Deployment aborted."
    exit 1
fi

# Start the application
echo "🎉 Starting application..."
echo "Application will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"

python app.py
