#!/usr/bin/env python
"""
Setup script for AI Vocabulary Assistant
Handles environment setup and initialization
"""

import os
import sys
import subprocess

def setup_environment():
    """Setup Python virtual environment and dependencies"""
    
    print("=" * 60)
    print("AI Vocabulary Assistant - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Create virtual environment
    if not os.path.exists('venv'):
        print("\n📦 Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment
    if sys.platform == 'win32':
        activate_script = 'venv\\Scripts\\activate.bat'
    else:
        activate_script = 'source venv/bin/activate'
    
    print(f"\n📝 To activate the virtual environment, run:")
    print(f"   {activate_script}")
    
    # Install requirements
    print("\n📥 Installing dependencies...")
    if sys.platform == 'win32':
        pip_path = 'venv\\Scripts\\pip'
    else:
        pip_path = 'venv/bin/pip'
    
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    print("✅ Dependencies installed")
    
    # Initialize database
    print("\n💾 Initializing database...")
    from database import init_db
    init_db()
    print("✅ Database initialized")
    
    print("\n" + "=" * 60)
    print("✨ Setup complete!")
    print("=" * 60)
    print("\nTo start the application, run:")
    print("   python app.py")
    print("\nThen open http://localhost:5000 in your browser")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        setup_environment()
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        sys.exit(1)
