from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
from config.settings import Config

# Get the project root directory (3 levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['DEBUG'] = Config.WEBSITE_DEBUG

# Vercel KV configuration
KV_URL = os.environ.get('KV_URL')
KV_REST_API_TOKEN = os.environ.get('KV_REST_API_TOKEN')

class VercelWebsite:
    """Website class using Vercel KV for persistent storage."""
    
    def __init__(self):
        self.articles = []
        self.comics = []
    
    def load_articles(self):
        """Load articles from Vercel KV."""
        try:
            import requests
            response = requests.get(
                f"{KV_URL}/kv/article:*",
                headers={
                    "Authorization": f"Bearer {KV_REST_API_TOKEN}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                articles_data = response.json()
                self.articles = []
                
                # Parse KV response to get articles
                for key, value in articles_data.items():
                    if key.startswith('article:'):
                        article = json.loads(value)
                        self.articles.append(article)
                
                # Sort by date (newest first)
                self.articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
                
            return self.articles
        except Exception as e:
            print(f"Error loading articles: {e}")
            return []
    
    def load_comics(self):
        """Load comics from Vercel KV."""
        try:
            import requests
            response = requests.get(
                f"{KV_URL}/kv/comic:*",
                headers={
                    "Authorization": f"Bearer {KV_REST_API_TOKEN}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                comics_data = response.json()
                self.comics = []
                
                # Parse KV response to get comics
                for key, value in comics_data.items():
                    if key.startswith('comic:'):
                        comic = json.loads(value)
                        self.comics.append(comic)
                
                # Sort by date (newest first)
                self.comics.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                
            return self.comics
        except Exception as e:
            print(f"Error loading comics: {e}")
            return []
    
    def save_article(self, article):
        """Save article to Vercel KV."""
        try:
            import requests
            article_key = f"article:{article.get('id', datetime.now().isoformat())}"
            
            response = requests.put(
                f"{KV_URL}/kv/{article_key}",
                headers={
                    "Authorization": f"Bearer {KV_REST_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                data=json.dumps(article)
            )
            
            if response.status_code == 200:
                self.articles.append(article)
                # Keep only most recent articles
                self.articles = self.articles[-Config.MAX_ARTICLES_STORED:]
                
            return response.status_code == 200
        except Exception as e:
            print(f"Error saving article: {e}")
            return False
    
    def save_comic(self, comic):
        """Save comic to Vercel KV."""
        try:
            import requests
            comic_key = f"comic:{comic.get('id', datetime.now().isoformat())}"
            
            response = requests.put(
                f"{KV_URL}/kv/{comic_key}",
                headers={
                    "Authorization": f"Bearer {KV_REST_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                data=json.dumps(comic)
            )
            
            if response.status_code == 200:
                self.comics.append(comic)
                # Keep only most recent comics
                self.comics = self.comics[-Config.MAX_COMICS_STORED:]
                
            return response.status_code == 200
        except Exception as e:
            print(f"Error saving comic: {e}")
            return False

# Initialize Vercel website
website = VercelWebsite()

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
    """Trigger news generation cycle."""
    try:
        # Import and run automation
        from src.schedulers.automation_scheduler import AutomationScheduler
        scheduler = AutomationScheduler()
        results = scheduler.run_cycle()
        
        # Store results in Vercel KV
        for article in results.get('articles', []):
            website.save_article(article)
        
        for comic in results.get('comics', []):
            website.save_comic(comic)
        
        return jsonify({
            "success": True,
            "message": f"Generated {len(results.get('articles', []))} articles and {len(results.get('comics', []))} comics",
            "results": results
        })
        
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
