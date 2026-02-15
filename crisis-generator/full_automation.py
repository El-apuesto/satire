#!/usr/bin/env python3
"""
Full Automation for OK Crisis News Site
Complete hands-off operation
"""

import requests
import json
import subprocess
import time
import schedule
from datetime import datetime
import os
import sys

class NewsSiteAutomation:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.surge_domain = "okcrisis-news.surge.sh"
        self.log_file = "automation.log"
        
    def log(self, message):
        """Log automation events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Save to log file with UTF-8 encoding
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    
    def check_server_health(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def generate_articles(self, category=None):
        """Generate new articles"""
        self.log(f"🔄 Generating articles{' for ' + category if category else ''}...")
        
        try:
            url = f"{self.base_url}/refresh-news"
            if category:
                url += f"?category={category}"
                
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log(f"✅ {data.get('message', 'Articles generated')}")
                    return True
                else:
                    self.log(f"❌ Failed to generate: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log(f"❌ Server error: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error generating articles: {str(e)}")
            return False
    
    def create_comic(self):
        """Create a new comic"""
        self.log("🎨 Creating new comic...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/create-comic",
                json={"headline": f"Daily Comic {datetime.now().strftime('%Y-%m-%d')}", "category": "daily"},
                timeout=30
            )
            
            if response.status_code == 200:
                self.log("✅ Comic created successfully")
                return True
            else:
                self.log(f"❌ Failed to create comic: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error creating comic: {str(e)}")
            return False
    
    def deploy_to_surge(self):
        """Deploy site to Surge"""
        self.log("🚀 Deploying to Surge...")
        
        try:
            # Change to web directory
            os.chdir("web")
            
            # Run surge command
            result = subprocess.run(
                ['surge', '--domain', self.surge_domain], 
                capture_output=True, 
                text=True,
                timeout=120
            )
            
            # Change back to parent directory
            os.chdir("..")
            
            if result.returncode == 0:
                self.log(f"✅ Deployed successfully to {self.surge_domain}")
                return True
            else:
                self.log(f"❌ Deployment failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Deployment error: {str(e)}")
            return False
    
    def get_site_stats(self):
        """Get current site statistics"""
        try:
            response = requests.get(f"{self.base_url}/api/latest", timeout=10)
            
            if response.status_code == 200:
                articles = response.json()
                stats = {
                    'total_articles': len(articles),
                    'categories': {}
                }
                
                for article in articles:
                    cat = article.get('category', 'unknown')
                    stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
                
                return stats
            else:
                return None
                
        except Exception as e:
            self.log(f"❌ Error getting stats: {str(e)}")
            return None
    
    def send_email_report(self, stats):
        """Send daily email report (placeholder)"""
        self.log("📧 Sending daily report...")
        
        # You can integrate with email service here
        report = f"""
        OK Crisis Daily Report - {datetime.now().strftime('%Y-%m-%d')}
        
        Total Articles: {stats['total_articles']}
        
        By Category:
        """
        
        for cat, count in stats['categories'].items():
            report += f"  - {cat.title()}: {count}\n"
        
        self.log("📊 Report generated:")
        self.log(report)
        
        # TODO: Add actual email sending functionality
        # import smtplib
        # from email.mime.text import MIMEText
        # ... email sending code ...
    
    def morning_routine(self):
        """6 AM morning routine"""
        self.log("🌅 Starting morning routine...")
        
        if not self.check_server_health():
            self.log("❌ Server is not running!")
            return
        
        # Generate politics articles
        self.generate_articles("politics")
        
        # Create morning comic
        self.create_comic()
        
        # Deploy updates
        self.deploy_to_surge()
        
        self.log("✅ Morning routine completed")
    
    def noon_routine(self):
        """12 PM noon routine"""
        self.log("☀️ Starting noon routine...")
        
        if not self.check_server_health():
            self.log("❌ Server is not running!")
            return
        
        # Generate tech articles
        self.generate_articles("technology")
        
        # Deploy updates
        self.deploy_to_surge()
        
        self.log("✅ Noon routine completed")
    
    def evening_routine(self):
        """6 PM evening routine"""
        self.log("🌆 Starting evening routine...")
        
        if not self.check_server_health():
            self.log("❌ Server is not running!")
            return
        
        # Generate lifestyle articles
        self.generate_articles("lifestyle")
        
        # Create evening comic
        self.create_comic()
        
        # Deploy updates
        self.deploy_to_surge()
        
        self.log("✅ Evening routine completed")
    
    def nightly_routine(self):
        """11 PM nightly routine"""
        self.log("🌙 Starting nightly routine...")
        
        if not self.check_server_health():
            self.log("❌ Server is not running!")
            return
        
        # Generate mixed content
        self.generate_articles()
        
        # Get stats and send report
        stats = self.get_site_stats()
        if stats:
            self.send_email_report(stats)
        
        # Final deployment of the day
        self.deploy_to_surge()
        
        self.log("✅ Nightly routine completed")
    
    def run_full_cycle(self):
        """Run complete automation cycle"""
        self.log("🚀 Starting full automation cycle...")
        
        routines = [
            ("Morning", self.morning_routine),
            ("Noon", self.noon_routine), 
            ("Evening", self.evening_routine),
            ("Nightly", self.nightly_routine)
        ]
        
        for name, routine in routines:
            self.log(f"⏰ Running {name} routine...")
            routine()
            time.sleep(5)  # Brief pause between routines
        
        self.log("🎉 Full automation cycle completed!")
    
    def setup_scheduler(self):
        """Setup automated scheduling"""
        self.log("⏰ Setting up automated scheduler...")
        
        # Schedule routines
        schedule.every().day.at("06:00").do(self.morning_routine)
        schedule.every().day.at("12:00").do(self.noon_routine)
        schedule.every().day.at("18:00").do(self.evening_routine)
        schedule.every().day.at("23:00").do(self.nightly_routine)
        
        self.log("✅ Scheduler configured:")
        self.log("  - 06:00: Morning routine (Politics + Comic)")
        self.log("  - 12:00: Noon routine (Technology)")
        self.log("  - 18:00: Evening routine (Lifestyle + Comic)")
        self.log("  - 23:00: Nightly routine (Mixed + Report)")
    
    def run_scheduler(self):
        """Run the scheduler continuously"""
        self.setup_scheduler()
        
        self.log("🤖 Automation scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.log("👋 Automation scheduler stopped by user")
    
    def start_server(self):
        """Start the Flask server"""
        self.log("🖥️ Starting Flask server...")
        
        try:
            # Change to web directory
            os.chdir("web")
            
            # Start server in background
            subprocess.Popen([sys.executable, "app.py"])
            
            # Change back to parent directory
            os.chdir("..")
            
            # Wait for server to start
            time.sleep(5)
            
            if self.check_server_health():
                self.log("✅ Server started successfully")
                return True
            else:
                self.log("❌ Server failed to start")
                return False
                
        except Exception as e:
            self.log(f"❌ Error starting server: {str(e)}")
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OK Crisis News Site Automation")
    parser.add_argument("--mode", choices=["once", "schedule", "server"], 
                       default="once", help="Automation mode")
    
    args = parser.parse_args()
    
    automation = NewsSiteAutomation()
    
    if args.mode == "once":
        automation.run_full_cycle()
    elif args.mode == "schedule":
        automation.run_scheduler()
    elif args.mode == "server":
        if automation.start_server():
            automation.run_scheduler()
