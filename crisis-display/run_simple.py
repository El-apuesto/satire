#!/usr/bin/env python3
"""
Simple launcher for OK Crisis website
"""

import subprocess
import sys
import os

# Kill any existing Flask processes
try:
    subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], check=True, shell=True)
except:
    pass

# Start simple app
print("🚀 Starting simple OK Crisis app...")
print("📍 Visit: http://localhost:5000")
print("📍 Press Ctrl+C to stop")

# Run simple_app.py
subprocess.run([sys.executable, 'simple_app.py'], cwd=os.path.dirname(__file__))
