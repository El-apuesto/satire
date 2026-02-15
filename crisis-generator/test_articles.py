#!/usr/bin/env python3
"""
Test article links to verify 404 fix
"""

import requests
import time

def test_article_links():
    """Test all article links"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing article links...")
    
    # Test sample article IDs
    test_ids = [1, 2, 3, "1", "2", "3"]
    
    for article_id in test_ids:
        url = f"{base_url}/article/{article_id}"
        print(f"Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Article {article_id}: SUCCESS")
            elif response.status_code == 404:
                print(f"❌ Article {article_id}: 404 NOT FOUND")
            else:
                print(f"⚠️ Article {article_id}: {response.status_code}")
        except Exception as e:
            print(f"❌ Article {article_id}: ERROR - {str(e)}")
        
        time.sleep(1)  # Brief pause between requests

if __name__ == "__main__":
    test_articles()
