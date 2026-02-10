from flask import Flask, render_template, jsonify
import logging
import json
import os
from datetime import datetime
from config.settings import Config

logger = logging.getLogger(__name__)

# Get the project root directory (3 levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['DEBUG'] = Config.WEBSITE_DEBUG

class Website:
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
    
    def save_article(self, article):
        """Save an article to the JSON file."""
        articles = self.load_articles()
        articles.append(article)
        
        # Keep only the most recent articles (configurable)
        from config.settings import Config
        articles = articles[-Config.MAX_ARTICLES_STORED:]
        
        with open(self.articles_file, 'w') as f:
            json.dump(articles, f, indent=2)
    
    def save_comic(self, comic):
        """Save a comic to the JSON file."""
        comics = self.load_comics()
        comics.append(comic)
        
        # Keep only the most recent comics (configurable)
        from config.settings import Config
        comics = comics[-Config.MAX_COMICS_STORED:]
        
        with open(self.comics_file, 'w') as f:
            json.dump(comics, f, indent=2)

website = Website()

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
        try:
            return render_template('article.html', article=article)
        except Exception as e:
            logger.error(f"Template error: {e}")
            return f"Template error: {e}", 500
    else:
        return "Article not found", 404

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
