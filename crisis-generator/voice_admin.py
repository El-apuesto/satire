#!/usr/bin/env python3
"""
Voice Admin for OK Crisis News Site
Control your satire news site with voice commands
"""

import speech_recognition as sr
import pyttsx3
import requests
import json
import time
from datetime import datetime

class VoiceAdmin:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.base_url = "http://localhost:5000"
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice command"""
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            
        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            self.speak("Sorry, speech service is down. Please check your internet connection.")
            return None
    
    def refresh_news(self):
        """Generate new articles"""
        self.speak("Refreshing news and generating new articles...")
        try:
            response = requests.get(f"{self.base_url}/refresh-news")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.speak(f"Generated {data.get('message', 'new articles')}")
                else:
                    self.speak("Failed to generate articles")
            else:
                self.speak("Server error while refreshing news")
        except Exception as e:
            self.speak(f"Error refreshing news: {str(e)}")
    
    def show_stats(self):
        """Display site statistics"""
        self.speak("Getting site statistics...")
        try:
            response = requests.get(f"{self.base_url}/api/latest")
            if response.status_code == 200:
                articles = response.json()
                count = len(articles)
                self.speak(f"You currently have {count} articles on the site")
                
                # Count by category
                categories = {}
                for article in articles:
                    cat = article.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                
                for cat, count in categories.items():
                    self.speak(f"{count} {cat} articles")
            else:
                self.speak("Couldn't fetch statistics")
        except Exception as e:
            self.speak(f"Error getting stats: {str(e)}")
    
    def create_comic(self):
        """Create a new comic"""
        self.speak("Creating a new comic...")
        try:
            response = requests.post(
                f"{self.base_url}/api/create-comic",
                json={"headline": "Voice Generated Comic", "category": "general"}
            )
            if response.status_code == 200:
                self.speak("Comic created successfully")
            else:
                self.speak("Failed to create comic")
        except Exception as e:
            self.speak(f"Error creating comic: {str(e)}")
    
    def deploy_site(self):
        """Deploy site to surge"""
        self.speak("Deploying site to surge...")
        import subprocess
        try:
            result = subprocess.run(['surge', '--domain', 'okcrisis-news.surge.sh'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.speak("Site deployed successfully to okcrisis-news.surge.sh")
            else:
                self.speak("Deployment failed")
        except Exception as e:
            self.speak(f"Deployment error: {str(e)}")
    
    def get_latest_articles(self):
        """Read latest article headlines"""
        self.speak("Getting latest articles...")
        try:
            response = requests.get(f"{self.base_url}/api/latest")
            if response.status_code == 200:
                articles = response.json()[:3]  # Get top 3
                for i, article in enumerate(articles, 1):
                    headline = article.get('headline', 'No headline')
                    self.speak(f"Article {i}: {headline}")
            else:
                self.speak("Couldn't fetch articles")
        except Exception as e:
            self.speak(f"Error fetching articles: {str(e)}")
    
    def process_command(self, command):
        """Process voice command"""
        if not command:
            return
            
        # Refresh news commands
        if any(word in command for word in ['refresh', 'new', 'generate', 'update']):
            self.refresh_news()
        
        # Statistics commands
        elif any(word in command for word in ['stats', 'statistics', 'count', 'how many']):
            self.show_stats()
        
        # Comic commands
        elif any(word in command for word in ['comic', 'make comic', 'create comic']):
            self.create_comic()
        
        # Deploy commands
        elif any(word in command for word in ['deploy', 'publish', 'upload']):
            self.deploy_site()
        
        # Read articles
        elif any(word in command for word in ['read', 'articles', 'headlines', 'news']):
            self.get_latest_articles()
        
        # Help
        elif any(word in command for word in ['help', 'commands', 'what can you do']):
            self.show_help()
        
        # Exit
        elif any(word in command for word in ['exit', 'quit', 'stop', 'bye']):
            self.speak("Goodbye! Shutting down voice admin.")
            return False
        
        else:
            self.speak("I didn't understand that command. Say 'help' for available commands.")
        
        return True
    
    def show_help(self):
        """Display available commands"""
        commands = [
            "Available voice commands:",
            "Say 'refresh' to generate new articles",
            "Say 'stats' to see site statistics", 
            "Say 'comic' to create a new comic",
            "Say 'deploy' to deploy the site",
            "Say 'read' to hear latest headlines",
            "Say 'help' for this menu",
            "Say 'exit' to quit"
        ]
        
        for command in commands:
            self.speak(command)
            time.sleep(0.5)
    
    def run(self):
        """Main voice admin loop"""
        self.speak("OK Crisis Voice Admin activated!")
        self.speak("Say 'help' for available commands or 'exit' to quit.")
        
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)
            time.sleep(1)

if __name__ == "__main__":
    try:
        admin = VoiceAdmin()
        admin.run()
    except KeyboardInterrupt:
        print("\n👋 Voice admin stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
