#!/usr/bin/env python3
"""
Manual Comic Upload Tool
Upload your own comics when free credits run out
"""

import json
import os
from datetime import datetime
import shutil

def upload_manual_comic(image_path, title, characters, dialogue):
    """Upload a manually created comic."""
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Load existing comics
    comics = []
    if os.path.exists('data/comics.json'):
        with open('data/comics.json', 'r') as f:
            comics = json.load(f)
    
    # Copy image to static folder
    static_dir = 'static/comics'
    os.makedirs(static_dir, exist_ok=True)
    
    image_filename = f"manual_{datetime.now().isoformat().replace(':', '-')}.png"
    static_image_path = os.path.join(static_dir, image_filename)
    
    try:
        shutil.copy2(image_path, static_image_path)
        
        # Create comic entry
        comic = {
            'id': f"manual_{datetime.now().isoformat()}",
            'title': title,
            'image_url': f"/static/comics/{image_filename}",
            'dialogue': dialogue,
            'characters': characters,
            'created_at': datetime.now().isoformat(),
            'type': 'manual'
        }
        
        # Add to comics list
        comics.insert(0, comic)  # Add to beginning
        
        # Keep only latest 50 comics
        comics = comics[:50]
        
        # Save updated comics
        with open('data/comics.json', 'w') as f:
            json.dump(comics, f, indent=2)
        
        print(f"✅ Manual comic uploaded: {title}")
        print(f"📁 Saved to: {static_image_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading comic: {e}")
        return False

def upload_batch_comics():
    """Upload multiple comics from a folder."""
    comics_folder = input("Enter path to comics folder: ")
    
    if not os.path.exists(comics_folder):
        print("❌ Folder not found!")
        return
    
    print(f"📁 Scanning {comics_folder}...")
    
    for filename in os.listdir(comics_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(comics_folder, filename)
            
            title = input(f"\nTitle for {filename}: ")
            characters = input("Characters (comma separated): ")
            dialogue = input("Dialogue/description: ")
            
            upload_manual_comic(image_path, title, characters, dialogue)

if __name__ == "__main__":
    print("🎨 Manual Comic Upload Tool")
    print("1. Upload single comic")
    print("2. Upload batch from folder")
    
    choice = input("Choose option (1 or 2): ")
    
    if choice == "1":
        image_path = input("Enter image path: ")
        title = input("Enter title: ")
        characters = input("Enter characters: ")
        dialogue = input("Enter dialogue: ")
        
        upload_manual_comic(image_path, title, characters, dialogue)
        
    elif choice == "2":
        upload_batch_comics()
        
    else:
        print("❌ Invalid choice!")
