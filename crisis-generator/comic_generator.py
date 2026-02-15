#!/usr/bin/env python3
"""
Comic Generator with Custom Parameters for OK Crisis
Create comics with specific themes, characters, and styles
"""

import requests
import json
from datetime import datetime

class ComicGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def create_comic(self, headline, category="general", style="deadpan", characters=2):
        """Create comic with custom parameters"""
        
        comic_data = {
            "headline": headline,
            "category": category,
            "style": style,
            "characters": characters,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"🎨 Creating comic: '{headline}'")
        print(f"   Category: {category}")
        print(f"   Style: {style}")
        print(f"   Characters: {characters}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/create-comic",
                json=comic_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Comic created successfully!")
                    return result
                else:
                    print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                    return result
            else:
                print(f"❌ Server error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def create_political_comic(self, topic):
        """Create political satire comic"""
        return self.create_comic(
            headline=f"Political Crisis: {topic}",
            category="politics",
            style="satirical",
            characters=3
        )
    
    def create_tech_comic(self, topic):
        """Create technology satire comic"""
        return self.create_comic(
            headline=f"Tech Disaster: {topic}",
            category="technology", 
            style="nerdy",
            characters=2
        )
    
    def create_lifestyle_comic(self, topic):
        """Create lifestyle satire comic"""
        return self.create_comic(
            headline=f"Modern Life: {topic}",
            category="lifestyle",
            style="relatable",
            characters=2
        )
    
    def create_daily_comic(self):
        """Create today's daily comic"""
        day_topics = {
            "Monday": "Monday Motivation Gone Wrong",
            "Tuesday": "Tuesday Blues", 
            "Wednesday": "Hump Day Horrors",
            "Thursday": "Almost Friday Anxiety",
            "Friday": "Weekend Dreams",
            "Saturday": "Saturday Regret",
            "Sunday": "Sunday Scaries"
        }
        
        today = datetime.now().strftime("%A")
        topic = day_topics.get(today, "Daily Crisis")
        
        return self.create_comic(
            headline=f"{today}'s Crisis: {topic}",
            category="daily",
            style="varied",
            characters=2
        )

def main():
    """Interactive comic generator"""
    generator = ComicGenerator()
    
    print("🎭 OK Crisis Comic Generator")
    print("=" * 40)
    
    while True:
        print("\nComic Options:")
        print("1. Custom Comic")
        print("2. Political Comic")
        print("3. Tech Comic")
        print("4. Lifestyle Comic")
        print("5. Daily Comic")
        print("6. Exit")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == "1":
            # Custom comic
            headline = input("Enter headline: ").strip()
            category = input("Enter category (politics/tech/lifestyle/general): ").strip() or "general"
            style = input("Enter style (deadpan/satirical/nerdy/relatable): ").strip() or "deadpan"
            characters = int(input("Number of characters (1-4): ").strip() or "2")
            
            generator.create_comic(headline, category, style, characters)
            
        elif choice == "2":
            topic = input("Enter political topic: ").strip()
            generator.create_political_comic(topic)
            
        elif choice == "3":
            topic = input("Enter tech topic: ").strip()
            generator.create_tech_comic(topic)
            
        elif choice == "4":
            topic = input("Enter lifestyle topic: ").strip()
            generator.create_lifestyle_comic(topic)
            
        elif choice == "5":
            generator.create_daily_comic()
            
        elif choice == "6":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
