#!/usr/bin/env python3
"""
Development setup script for DFA Minimizer Web Application
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      capture_output=True, check=True)
        print("✅ pip is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip is not available")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies from requirements.txt...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    try:
        result = subprocess.run([sys.executable, 'run_tests.py'], 
                               capture_output=False, check=False)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 DFA Minimizer Web Application Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Run tests
    if not run_tests():
        print("⚠️  Setup completed but some tests failed")
        print("   You may still run the application with: python app.py")
        return False
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run the application: python app.py")
    print("   2. Open your browser to: http://localhost:5000")
    print("   3. Try the example DFAs to get started")
    print("\n📚 For more information, see README.md")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
