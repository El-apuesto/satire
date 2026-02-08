#!/usr/bin/env python3
"""
Main entry point for the Satire News Publishing System.

This script provides different modes of operation:
- scheduler: Run the automated twice-daily publishing system
- website: Run the Flask website server
- test: Run a test cycle to verify system functionality
- manual: Run a single publishing cycle manually

Usage:
    python main.py [mode]
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.schedulers.automation_scheduler import AutomationScheduler
from src.website.app import app
from config.settings import Config

def setup_logging():
    """Setup logging configuration."""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def run_scheduler():
    """Run the automated scheduler."""
    print("Starting Satire News Automation Scheduler...")
    print(f"Scheduled runs: {Config.MORNING_RUN_TIME} and {Config.EVENING_RUN_TIME}")
    print("Press Ctrl+C to stop")
    
    scheduler = AutomationScheduler()
    scheduler.start_scheduler()

def run_website():
    """Run the Flask website."""
    print("Starting Satire News Website...")
    print(f"Server: http://{Config.WEBSITE_HOST}:{Config.WEBSITE_PORT}")
    print("Press Ctrl+C to stop")
    
    app.run(
        host=Config.WEBSITE_HOST,
        port=Config.WEBSITE_PORT,
        debug=Config.WEBSITE_DEBUG
    )

def run_test():
    """Run a test cycle."""
    print("Running test cycle...")
    
    scheduler = AutomationScheduler()
    scheduler.run_test_cycle()
    
    print("Test cycle completed. Check the logs for details.")

def run_manual():
    """Run a manual publishing cycle."""
    print("Running manual publishing cycle...")
    
    scheduler = AutomationScheduler()
    scheduler.run_publishing_cycle("manual")
    
    print("Manual cycle completed. Check the logs for details.")

def show_help():
    """Show usage help."""
    print("""
Satire News Publishing System

USAGE:
    python main.py [mode]

MODES:
    scheduler  - Run the automated twice-daily publishing system
    website    - Run the Flask website server
    test       - Run a test cycle to verify system functionality
    manual     - Run a single publishing cycle manually
    help       - Show this help message

EXAMPLES:
    python main.py scheduler
    python main.py website
    python main.py test
    python main.py manual

CONFIGURATION:
    Copy .env.example to .env and configure your API keys
    Ensure all required services are accessible

WEBSITE ACCESS:
    Once running, visit http://localhost:5000 to view the published content
""")

def main():
    """Main entry point."""
    setup_logging()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    mode = sys.argv[1].lower()
    
    if mode in ['scheduler', 'schedule', 'auto']:
        run_scheduler()
    elif mode in ['website', 'web', 'server']:
        run_website()
    elif mode in ['test', 'debug']:
        run_test()
    elif mode in ['manual', 'run']:
        run_manual()
    elif mode in ['help', '--help', '-h']:
        show_help()
    else:
        print(f"Unknown mode: {mode}")
        show_help()

if __name__ == '__main__':
    main()
