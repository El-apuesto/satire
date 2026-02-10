import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the satire news publishing system."""
    
    # News API Configuration
    NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')
    NEWSDATA_API_URL = os.getenv('NEWSDATA_API_URL', 'https://newsdata.io/api/1/news')
    
    # Gemini AI Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    GEMINI_API_URL = os.getenv('GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models')
    
    # Image Generation Configuration
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
    UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
    
    # Website Configuration
    WEBSITE_HOST = os.getenv('WEBSITE_HOST', 'localhost')
    WEBSITE_PORT = int(os.getenv('WEBSITE_PORT', 5000))
    WEBSITE_DEBUG = os.getenv('WEBSITE_DEBUG', 'false').lower() == 'true'
    
    # Scheduling Configuration
    MORNING_RUN_TIME = os.getenv('MORNING_RUN_TIME', '08:00')
    EVENING_RUN_TIME = os.getenv('EVENING_RUN_TIME', '20:00')
    TIMEZONE = os.getenv('TIMEZONE', 'CST')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/satire_news.log')
    
    # Content Configuration
    ARTICLES_PER_CYCLE = int(os.getenv('ARTICLES_PER_CYCLE', 8))  # Increased to 8 for 2-5 per category
    COMICS_PER_CYCLE = int(os.getenv('COMICS_PER_CYCLE', 2))
    MAX_NEWS_STORIES = int(os.getenv('MAX_NEWS_STORIES', 30))  # Increased to 30 (5 per category x 6 categories)
    
    # Storage Limits
    MAX_ARTICLES_STORED = int(os.getenv('MAX_ARTICLES_STORED', 50))
    MAX_COMICS_STORED = int(os.getenv('MAX_COMICS_STORED', 20))
    MAX_IMAGES_STORED = int(os.getenv('MAX_IMAGES_STORED', 100))
    MAX_COMIC_IMAGES_STORED = int(os.getenv('MAX_COMIC_IMAGES_STORED', 50))
    
    # News Categories
    NEWS_CATEGORIES = ['world', 'politics', 'business', 'sports', 'entertainment', 'lifestyle']
    
    # Satire Styles
    SATIRE_STYLES = ['deadpan', 'absurdist', 'ironic', 'parody', 'exaggeration']
    
    # Satire Styles (now Sarcastic Reporting Styles)
    SARCASTIC_STYLES = ['sarcastic', 'smug', 'deadpan', 'cynical', 'world-weary']
    
    # Image Dimensions
    ARTICLE_IMAGE_WIDTH = 800
    ARTICLE_IMAGE_HEIGHT = 600
    COMIC_STRIP_WIDTH = 800
    COMIC_STRIP_HEIGHT = 400
