import requests
import json
from datetime import datetime
import os

class NewsDataAPI:
    def __init__(self):
        self.api_key = os.getenv('NEWSDATA_API_KEY', 'demo-key')
        self.base_url = 'https://newsdata.io/api/1/news'
    
    def fetch_latest_news(self, category=None, country='us', limit=10):
        """Fetch latest news articles"""
        try:
            params = {
                'apikey': self.api_key,
                'country': country,
                'language': 'en',
                'size': limit
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self.format_articles(data.get('results', []))
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def format_articles(self, raw_articles):
        """Format raw news articles into our format"""
        formatted = []
        
        for article in raw_articles:
            formatted_article = {
                'title': article.get('title', ''),
                'content': article.get('content', article.get('description', '')),
                'source': article.get('source_id', ''),
                'category': article.get('category', ['general'])[0],
                'published_date': article.get('pubDate', ''),
                'url': article.get('link', ''),
                'image_url': article.get('image_url', '')
            }
            formatted.append(formatted_article)
        
        return formatted
    
    def get_categories(self):
        """Get available news categories"""
        return [
            'politics', 'technology', 'science', 'health', 
            'sports', 'entertainment', 'business', 'world'
        ]
