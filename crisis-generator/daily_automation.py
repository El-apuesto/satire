#!/usr/bin/env python3
"""
Simple Daily Automation for OK Crisis News
Runs automatically every day to generate content and deploy
"""

import requests
import subprocess
import time
from datetime import datetime
import os

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def generate_content():
    """Generate new articles and deploy"""
    log("Starting daily content generation...")
    
    # Start the server first
    log("Starting server...")
    os.chdir("web")
    server_process = subprocess.Popen(["python", "app.py"])
    time.sleep(10)  # Wait for server to start
    
    try:
        # Generate new articles
        log("Generating new articles...")
        response = requests.get("http://localhost:5000/refresh-news", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                log(f"SUCCESS: {data.get('message', 'Articles generated')}")
            else:
                log(f"FAILED: {data.get('message', 'Unknown error')}")
        else:
            log(f"FAILED: Server returned {response.status_code}")
        
        # Deploy to surge
        log("Deploying to Surge...")
        result = subprocess.run(
            ['surge', '--domain', 'okcrisis-news.surge.sh'], 
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            log("SUCCESS: Site deployed to okcrisis-news.surge.sh")
        else:
            log(f"FAILED: Deployment error - {result.stderr}")
            
    finally:
        # Stop server
        server_process.terminate()
        os.chdir("..")
    
    log("Daily automation completed!")

if __name__ == "__main__":
    log("=== OK Crisis Daily Automation Started ===")
    generate_content()
    log("=== Automation Complete ===")
