#!/usr/bin/env python3
"""
Deployment script for PythonAnywhere
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required files exist for deployment."""
    required_files = [
        'main.py',
        'requirements.txt',
        '.env',
        'config/settings.py',
        'src/',
        'templates/',
        'static/'
    ]
    
    missing = []
    for item in required_files:
        if not os.path.exists(item):
            missing.append(item)
    
    if missing:
        print("❌ Missing required files:")
        for item in missing:
            print(f"  - {item}")
        return False
    
    print("✅ All required files present")
    return True

def create_pythonanywhere_config():
    """Create PythonAnywhere configuration files."""
    
    # Create wsgi.py for PythonAnywhere
    wsgi_content = '''import sys
import os

# Add the project directory to the Python path
project_home = u'/home/yourusername/yourdomain.com'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import the Flask app
from src.website.app import app as application

# Set environment variables
os.environ['GROQ_API_KEY'] = 'your-groq-key-here'
os.environ['NEWSDATA_API_KEY'] = 'pub_39e106ccf96046c5bfe5d6dd1d9f6bed'
'''
    
    with open('wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    print("✅ Created wsgi.py for PythonAnywhere")

def create_requirements():
    """Create requirements.txt for deployment."""
    requirements = '''flask==2.3.3
python-dotenv==1.0.0
requests==2.31.0
groq==0.11.0
Pillow==10.1.0
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Updated requirements.txt for deployment")

def main():
    """Main deployment setup."""
    print("🚀 Setting up OK Crisis for PythonAnywhere deployment...")
    
    if not check_requirements():
        sys.exit(1)
    
    create_pythonanywhere_config()
    create_requirements()
    
    print("\n📋 Next Steps:")
    print("1. Sign up at https://www.pythonanywhere.com/")
    print("2. Create a new Web application")
    print("3. Choose 'Manual Configuration' → 'Flask'")
    print("4. Upload your project files")
    print("5. Set wsgi.py as your WSGI file")
    print("6. Add your GROQ_API_KEY to environment variables")
    print("7. Set up a scheduled task for automation")
    print("8. Reload the web app")
    print("\n🎯 Your OK Crisis will be live!")

if __name__ == "__main__":
    main()
