#!/usr/bin/env python3
"""
Sync generated content to GitHub
"""

import os
import subprocess
from datetime import datetime

def sync_to_github():
    """Sync data files to GitHub."""
    print("🔄 Syncing content to GitHub...")
    
    try:
        # Add data files
        subprocess.run(['git', 'add', 'data/'], check=True)
        
        # Commit with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(['git', 'commit', '-m', f'Update content - {timestamp}'], check=True)
        
        # Push to display branch
        subprocess.run(['git', 'push', 'origin', 'display'], check=True)
        
        print("✅ Content synced to GitHub!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error syncing: {e}")

if __name__ == "__main__":
    sync_to_github()
