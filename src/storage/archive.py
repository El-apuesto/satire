import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class ArchiveManager:
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self.articles_file = os.path.join(self.storage_path, 'articles.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Load existing articles
        self.articles = self.load_articles()
    
    def load_articles(self) -> List[Dict[str, Any]]:
        """Load articles from storage"""
        try:
            if os.path.exists(self.articles_file):
                with open(self.articles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading articles: {e}")
            return []
    
    def save_articles(self) -> bool:
        """Save articles to storage"""
        try:
            with open(self.articles_file, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving articles: {e}")
            return False
    
    def add_article(self, article: Dict[str, Any]) -> bool:
        """Add a new article to the archive"""
        try:
            # Check if article already exists
            existing_ids = [a.get('id') for a in self.articles]
            if article.get('id') in existing_ids:
                return False
            
            # Add timestamp if not present
            if 'timestamp' not in article:
                article['timestamp'] = datetime.now().isoformat()
            
            self.articles.append(article)
            return self.save_articles()
        except Exception as e:
            print(f"Error adding article: {e}")
            return False
    
    def search_articles(self, query: str = "", category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search articles by query and/or category"""
        try:
            filtered_articles = self.articles
            
            # Filter by category
            if category:
                filtered_articles = [a for a in filtered_articles if a.get('category', '').lower() == category.lower()]
            
            # Filter by query (search in headline and content)
            if query:
                query = query.lower()
                filtered_articles = [a for a in filtered_articles if 
                    query in a.get('headline', '').lower() or 
                    query in a.get('opening_paragraph', '').lower()]
            
            # Sort by timestamp (newest first)
            filtered_articles.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Limit results
            return filtered_articles[:limit]
        except Exception as e:
            print(f"Error searching articles: {e}")
            return []
    
    def get_article_by_id(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific article by ID"""
        try:
            for article in self.articles:
                if article.get('id') == article_id:
                    return article
            return None
        except Exception as e:
            print(f"Error getting article by ID: {e}")
            return None
    
    def get_related_articles(self, article: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """Get related articles based on category"""
        try:
            category = article.get('category', '')
            current_id = article.get('id')
            
            # Get articles from same category (excluding current)
            related = [a for a in self.articles 
                       if a.get('category', '').lower() == category.lower() 
                       and a.get('id') != current_id]
            
            # Sort by timestamp and limit
            related.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return related[:limit]
        except Exception as e:
            print(f"Error getting related articles: {e}")
            return []
    
    def get_latest_articles(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Get the latest articles"""
        try:
            sorted_articles = sorted(self.articles, key=lambda x: x.get('timestamp', ''), reverse=True)
            return sorted_articles[:limit]
        except Exception as e:
            print(f"Error getting latest articles: {e}")
            return []
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            categories = set()
            for article in self.articles:
                if article.get('category'):
                    categories.add(article.get('category').lower())
            return sorted(list(categories))
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def get_article_count(self) -> int:
        """Get total number of articles"""
        return len(self.articles)
    
    def delete_old_articles(self, days: int = 30) -> int:
        """Delete articles older than specified days"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            original_count = len(self.articles)
            self.articles = [a for a in self.articles 
                           if datetime.fromisoformat(a.get('timestamp', '').replace('Z', '+00:00')) > cutoff_date]
            
            deleted_count = original_count - len(self.articles)
            if deleted_count > 0:
                self.save_articles()
            
            return deleted_count
        except Exception as e:
            print(f"Error deleting old articles: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get archive statistics"""
        try:
            stats = {
                'total_articles': len(self.articles),
                'categories': self.get_categories(),
                'latest_article': None,
                'articles_by_category': {}
            }
            
            # Count articles by category
            for article in self.articles:
                category = article.get('category', 'unknown')
                stats['articles_by_category'][category] = stats['articles_by_category'].get(category, 0) + 1
            
            # Get latest article
            if self.articles:
                latest = max(self.articles, key=lambda x: x.get('timestamp', ''))
                stats['latest_article'] = {
                    'headline': latest.get('headline', ''),
                    'timestamp': latest.get('timestamp', ''),
                    'category': latest.get('category', '')
                }
            
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
