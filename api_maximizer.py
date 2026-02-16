#!/usr/bin/env python3
"""
Maximize API Usage Script
Fetches news from all categories throughout the day to find the best content
"""

import requests
import time
import random
from datetime import datetime

class APIMaximizer:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.categories = [
            'politics', 'technology', 'science', 'sports', 'entertainment',
            'business', 'finance', 'health', 'world', 'lifestyle'
        ]
        self.hot_topics = [
            'super bowl', 'nfl', 'tom brady', 'epstein', 'trump', 'biden',
            'election', 'economy', 'inflation', 'crypto', 'ai', 'climate',
            'ukraine', 'israel', 'china', 'russia', 'supreme court'
        ]
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def check_server(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def fetch_category_news(self, category):
        """Fetch news for specific category"""
        try:
            url = f"{self.base_url}/refresh-news"
            if category:
                url += f"?category={category}"
                
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ {category}: {data.get('message', 'Success')}")
                return data.get('success', False)
            else:
                self.log(f"❌ {category}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ {category}: Error - {str(e)}")
            return False
    
    def run_continuous_mode(self):
        """Run continuously to maximize API usage"""
        self.log("🚀 Starting API Maximizer - Continuous Mode")
        
        cycle_count = 0
        while True:
            cycle_count += 1
            self.log(f"\n📊 Cycle {cycle_count} - Fetching from all categories")
            
            # Shuffle categories for variety
            shuffled_categories = self.categories.copy()
            random.shuffle(shuffled_categories)
            
            success_count = 0
            for category in shuffled_categories:
                if self.fetch_category_news(category):
                    success_count += 1
                
                # Small delay between requests
                time.sleep(2)
            
            self.log(f"📈 Cycle {cycle_count} complete: {success_count}/{len(shuffled_categories)} successful")
            
            # Wait before next cycle (10 minutes)
            self.log("⏳ Waiting 10 minutes before next cycle...")
            time.sleep(600)
    
    def run_burst_mode(self):
        """Run burst mode to quickly generate content"""
        self.log("⚡ Starting API Maximizer - Burst Mode")
        
        # Fetch from all categories once
        success_count = 0
        for category in self.categories:
            if self.fetch_category_news(category):
                success_count += 1
            time.sleep(1)  # Quick burst
        
        self.log(f"🎯 Burst complete: {success_count}/{len(self.categories)} successful")
        
        # Fetch hot topics (multiple rounds)
        for round_num in range(3):
            self.log(f"🔥 Hot Topics Round {round_num + 1}")
            for category in ['politics', 'world', 'entertainment']:
                if self.fetch_category_news(category):
                    success_count += 1
                time.sleep(1)
    
    def run_smart_mode(self):
        """Smart mode - focus on high-value categories"""
        self.log("🧠 Starting API Maximizer - Smart Mode")
        
        # Priority categories (more likely to have juicy content)
        priority_categories = ['politics', 'world', 'entertainment', 'sports', 'business']
        
        # Multiple rounds for priority categories
        for round_num in range(3):
            self.log(f"🎯 Priority Round {round_num + 1}")
            for category in priority_categories:
                if self.fetch_category_news(category):
                    success_count += 1
                time.sleep(2)
        
        # One round of other categories
        self.log("📰 Standard Categories")
        other_categories = ['technology', 'science', 'health', 'finance', 'lifestyle']
        for category in other_categories:
            if self.fetch_category_news(category):
                success_count += 1
            time.sleep(2)

if __name__ == "__main__":
    import sys
    
    if not requests.get("http://localhost:5000/").ok:
        print("❌ Server not running! Please start the Flask server first.")
        sys.exit(1)
    
    maximizer = APIMaximizer()
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "smart"
    
    if mode == "continuous":
        maximizer.run_continuous_mode()
    elif mode == "burst":
        maximizer.run_burst_mode()
    elif mode == "smart":
        maximizer.run_smart_mode()
    else:
        print("Usage: python api_maximizer.py [continuous|burst|smart]")
        print("  continuous - Run continuously (10 min cycles)")
        print("  burst      - Quick burst of all categories")
        print("  smart      - Focus on high-value categories (default)")
