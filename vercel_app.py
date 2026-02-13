from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
from config.settings import Config

# For Vercel deployment, templates should be in the same directory
app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = Config.WEBSITE_DEBUG

# Redis configuration
REDIS_URL = os.environ.get('REDIS_URL')

class SimpleWebsite:
    """Website class using simple file storage for Vercel."""
    
    def __init__(self):
        self.data_dir = "data"
        self.articles_file = os.path.join(self.data_dir, "articles.json")
        self.comics_file = os.path.join(self.data_dir, "comics.json")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self._init_data_files()
    
    def _init_data_files(self):
        """Initialize empty data files if they don't exist."""
        if not os.path.exists(self.articles_file):
            with open(self.articles_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.comics_file):
            with open(self.comics_file, 'w') as f:
                json.dump([], f)
    
    def load_articles(self):
        """Load articles from JSON file."""
        try:
            with open(self.articles_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def load_comics(self):
        """Load comics from JSON file."""
        try:
            with open(self.comics_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_articles(self, articles):
        """Save articles to JSON file."""
        try:
            with open(self.articles_file, 'w') as f:
                json.dump(articles, f)
        except:
            pass
    
    def save_comics(self, comics):
        """Save comics to JSON file."""
        try:
            with open(self.comics_file, 'w') as f:
                json.dump(comics, f)
        except:
            pass
        
        if REDIS_URL:
            try:
                import redis
                self.redis_client = redis.from_url(REDIS_URL)
            except Exception as e:
                print(f"Redis connection error: {e}")
    
    def load_articles(self):
        """Load articles from Redis."""
        try:
            if not self.redis_client:
                return []
                
            # Get all article keys
            article_keys = self.redis_client.keys("article:*")
            self.articles = []
            
            for key in article_keys:
                article_data = self.redis_client.get(key)
                if article_data:
                    article = json.loads(article_data)
                    self.articles.append(article)
            
            # Sort by date (newest first)
            self.articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
            return self.articles
        except Exception as e:
            print(f"Error loading articles: {e}")
            return []
    
    def load_comics(self):
        """Load comics from Redis."""
        try:
            if not self.redis_client:
                return []
                
            # Get all comic keys
            comic_keys = self.redis_client.keys("comic:*")
            self.comics = []
            
            for key in comic_keys:
                comic_data = self.redis_client.get(key)
                if comic_data:
                    comic = json.loads(comic_data)
                    self.comics.append(comic)
            
            # Sort by date (newest first)
            self.comics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return self.comics
        except Exception as e:
            print(f"Error loading comics: {e}")
            return []
    
    def save_article(self, article):
        """Save article to Redis."""
        try:
            if not self.redis_client:
                return False
                
            article_key = f"article:{article.get('id', datetime.now().isoformat())}"
            self.redis_client.set(article_key, json.dumps(article))
            
            self.articles.append(article)
            # Keep only most recent articles
            self.articles = self.articles[-Config.MAX_ARTICLES_STORED:]
            
            return True
        except Exception as e:
            print(f"Error saving article: {e}")
            return False
    
    def save_comic(self, comic):
        """Save comic to Redis."""
        try:
            if not self.redis_client:
                return False
                
            comic_key = f"comic:{comic.get('id', datetime.now().isoformat())}"
            self.redis_client.set(comic_key, json.dumps(comic))
            
            self.comics.append(comic)
            # Keep only most recent comics
            self.comics = self.comics[-Config.MAX_COMICS_STORED:]
            
            return True
        except Exception as e:
            print(f"Error saving comic: {e}")
            return False

# Initialize website
website = SimpleWebsite()

@app.route('/')
def home():
    """Home page with latest articles and comics."""
    articles = website.load_articles()
    comics = website.load_comics()
    
    # Get latest 6 articles and 3 comics
    latest_articles = articles[:6] if articles else []
    latest_comics = comics[:3] if comics else []
    
    return render_template('index.html', 
                         articles=latest_articles, 
                         comics=latest_comics)

@app.route('/articles')
def articles():
    """Articles page showing all articles."""
    articles = website.load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/comics')
def comics():
    """Comics page showing all comics."""
    comics = website.load_comics()
    return render_template('comics.html', comics=comics)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    """Individual article page."""
    articles = website.load_articles()
    
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        return render_template('article.html', article=article)
    else:
        return "Article not found", 404

@app.route('/admin')
def admin():
    """Admin dashboard."""
    return render_template('admin_dashboard.html')

@app.route('/run_cycle', methods=['GET'])
def run_cycle():
    """Simple news generation using real APIs."""
    try:
        # Import API keys
        from config.settings import Config
        
        # Fetch real news
        import requests
        news_response = requests.get(
            'https://newsdata.io/api/1/news',
            params={
                'apikey': Config.NEWSDATA_API_KEY,
                'country': 'us',
                'category': 'technology',
                'size': 5
            }
        )
        
        if news_response.status_code == 200:
            news_data = news_response.json()
            articles = []
            
            # Generate satire for each news story
            for story in news_data.get('results', [])[:2]:
                try:
                    # Use Groq AI for satire generation
                    import requests
                    groq_response = requests.post(
                        'https://api.groq.com/openai/v1/chat/completions',
                        headers={
                            'Authorization': f'Bearer {Config.GROQ_API_KEY}',
                            'Content-Type': 'application/json'
                        },
                        json={
                            'model': 'llama-3.1-8b-instant',
                            'messages': [
                                {
                                    'role': 'user',
                                    'content': f'Turn this news story into satire: {story.get("title", "")} - {story.get("description", "")}'
                                }
                            ],
                            'temperature': 0.7
                        }
                    )
                    
                    if groq_response.status_code == 200:
                        ai_content = groq_response.json()['choices'][0]['message']['content']
                        
                        article = {
                            'id': datetime.now().isoformat(),
                            'title': f'Satire: {story.get("title", "Unknown")}',
                            'byline': 'AI Staff Writer',
                            'content': ai_content,
                            'satire_style': 'sarcastic',
                            'original_title': story.get('title', ''),
                            'original_source': 'NewsData API',
                            'category': story.get('category', 'general'),
                            'published_at': datetime.now().strftime('%Y-%m-%d'),
                            'word_count': len(ai_content.split()),
                            'created_at': datetime.now().isoformat()
                        }
                        
                        articles.append(article)
                        
                except Exception as e:
                    print(f"Error generating satire: {e}")
                    continue
            
            # Store articles in Redis
            if REDIS_URL:
                import redis
                redis_client = redis.from_url(REDIS_URL)
                for article in articles:
                    article_key = f"article:{article['id']}"
                    redis_client.set(article_key, json.dumps(article))
            
            return jsonify({
                "success": True,
                "message": f"Generated {len(articles)} satirical articles from real news",
                "results": {
                    "articles": articles,
                    "comics": []
                }
            })
            
        else:
            return jsonify({
                "success": False,
                "error": "Failed to fetch news"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Generation error: {str(e)}"
        }), 500

@app.route('/api/articles')
def api_articles():
    """API endpoint for articles."""
    articles = website.load_articles()
    return jsonify(articles)

@app.route('/api/comics')
def api_comics():
    """API endpoint for comics."""
    comics = website.load_comics()
    return jsonify(comics)

if __name__ == '__main__':
    app.run(host=Config.WEBSITE_HOST, port=Config.WEBSITE_PORT, debug=Config.WEBSITE_DEBUG)
