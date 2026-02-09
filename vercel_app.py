from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
from config.settings import Config

# Get the project root directory (3 levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['DEBUG'] = Config.WEBSITE_DEBUG

class CloudWebsite:
    """Website class for cloud deployment without file system writes."""
    
    def __init__(self):
        # Use in-memory storage for cloud deployment
        self.articles = []
        self.comics = []
    
    def load_articles(self):
        """Load articles from memory storage."""
        return self.articles
    
    def load_comics(self):
        """Load comics from memory storage."""
        return self.comics
    
    def save_article(self, article):
        """Save article to memory storage."""
        self.articles.append(article)
        # Keep only the most recent articles
        self.articles = self.articles[-Config.MAX_ARTICLES_STORED:]
    
    def save_comic(self, comic):
        """Save comic to memory storage."""
        self.comics.append(comic)
        # Keep only the most recent comics
        self.comics = self.comics[-Config.MAX_COMICS_STORED:]

# Initialize cloud website
website = CloudWebsite()

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

# Add some sample content for demonstration
def add_sample_content():
    """Add sample content for cloud deployment demonstration."""
    sample_article = {
        'title': 'Local Man Discovers Weather Changes Seasonally, Scientists Baffled',
        'byline': 'Skip McGee, Staff Writer',
        'content': '''In a stunning development that has meteorologists scratching their heads, local resident Barry Thompson, 47, reportedly noticed that the weather tends to change with the seasons.

"Oh, you don't say," said Thompson from his porch, where he was observing what experts now confirm is called "winter." "It's cold in December and warm in July. Groundbreaking stuff, really."

Scientists at the National Weather Service, when informed of Thompson's discovery, were reportedly shocked. "We had no idea," said Dr. Patricia Winklestein, lead climatologist. "All our sophisticated equipment and decades of research, and it turns out some guy just figured it out by looking outside."

The revelation has prompted calls for a complete overhaul of weather forecasting methodology. "Why spend millions on satellites when we could just ask Barry what he thinks?" questioned one congressional representative.

Thompson, for his part, remains humble about his contribution to atmospheric science. "I'm just a regular guy who noticed it gets cold when the days get shorter. I'm sure someone would have figured it out eventually."

In related news, water has been confirmed to be wet, and fire has been found to be hot. More at 11.''',
        'satire_style': 'sarcastic',
        'original_title': 'Seasonal Weather Patterns Continue as Expected',
        'original_source': 'Local Weather Service',
        'category': 'lifestyle',
        'published_at': '2024-02-07',
        'word_count': 156,
        'created_at': datetime.now().isoformat()
    }
    
    sample_comic = {
        'title': 'Weather Discovery Comic',
        'image_path': None,
        'description': 'Barry Thompson discovers seasons exist',
        'created_at': datetime.now().isoformat()
    }
    
    website.save_article(sample_article)
    website.save_comic(sample_comic)

# Add sample content on startup
add_sample_content()

if __name__ == '__main__':
    app.run(host=Config.WEBSITE_HOST, port=Config.WEBSITE_PORT, debug=Config.WEBSITE_DEBUG)
