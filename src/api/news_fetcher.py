import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config.settings import Config

logger = logging.getLogger(__name__)

class NewsFetcher:
    """Fetches news stories from NewsData.io API."""
    
    def __init__(self):
        self.api_key = Config.NEWSDATA_API_KEY
        self.base_url = Config.NEWSDATA_API_URL
        self.categories = Config.NEWS_CATEGORIES
        
    def fetch_news(self, hours_back: int = 12, max_stories: int = None) -> List[Dict]:
        """
        Fetch news stories from the last specified hours.
        
        Args:
            hours_back: Number of hours to look back for news
            max_stories: Maximum number of stories to fetch
            
        Returns:
            List of news story dictionaries
        """
        if not self.api_key:
            logger.error("NewsData.io API key not configured")
            return []
            
        max_stories = max_stories or Config.MAX_NEWS_STORIES
        stories = []
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=hours_back)
        
        for category in self.categories:
            try:
                params = {
                    'apikey': self.api_key,
                    'language': 'en',
                    'category': category,
                    'size': 5  # Get 5 stories per category
                }
                
                logger.info(f"Fetching {category} news from {start_date} to {end_date}")
                
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'success' and 'results' in data:
                    category_stories = data['results']
                    for story in category_stories:
                        story['fetched_category'] = category
                        story['fetched_at'] = datetime.now().isoformat()
                    stories.extend(category_stories)
                    logger.info(f"Fetched {len(category_stories)} {category} stories")
                else:
                    logger.warning(f"No successful response for {category}: {data}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {category} news: {e}")
            except Exception as e:
                logger.error(f"Unexpected error fetching {category} news: {e}")
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_stories = []
        for story in stories:
            title = story.get('title', '').lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_stories.append(story)
        
        # Limit to max_stories
        final_stories = unique_stories[:max_stories]
        
        logger.info(f"Total unique stories fetched: {len(final_stories)}")
        return final_stories
    
    def get_story_summary(self, story: Dict) -> Dict:
        """
        Extract key information from a news story.
        
        Args:
            story: News story dictionary
            
        Returns:
            Dictionary with story summary
        """
        return {
            'title': story.get('title', ''),
            'description': story.get('description', ''),
            'content': story.get('content', ''),
            'source': story.get('source_id', ''),
            'category': story.get('fetched_category', ''),
            'published_at': story.get('pubDate', ''),
            'url': story.get('link', ''),
            'image_url': story.get('image_url', ''),
            'keywords': story.get('keywords', []),
            'creator': story.get('creator', [])
        }
    
    def validate_story(self, story: Dict) -> bool:
        """
        Validate that a story has minimum required fields.
        
        Args:
            story: News story dictionary
            
        Returns:
            True if story is valid, False otherwise
        """
        required_fields = ['title', 'description']
        for field in required_fields:
            if not story.get(field):
                logger.warning(f"Story missing required field '{field}': {story.get('title', 'Unknown')}")
                return False
        
        # Filter out very short or low-quality content
        title = story.get('title', '')
        description = story.get('description', '')
        
        if len(title) < 10 or len(description) < 20:
            logger.warning(f"Story too short: {title}")
            return False
            
        return True
