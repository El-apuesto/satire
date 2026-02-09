from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

# Flask app for PythonAnywhere deployment
app = Flask(__name__)

# Set template path to current directory
app.template_folder = 'templates'

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
            return f"Template error: {e}", 500
    else:
        return "Article not found", 404

@app.route('/run-cycle')
def run_cycle():
    """Trigger manual news cycle via webhook."""
    import subprocess
    import json
    
    if request.method == 'GET':
        return '''
        <h1>OK Crisis Manual Cycle Trigger</h1>
        <p>Use POST request to run cycle, or click the button below:</p>
        <form method="POST">
            <button type="submit">Run News Cycle</button>
        </form>
        '''
    
    try:
        # Run the automation
        result = subprocess.run(['python', 'main.py', 'manual'], 
                              capture_output=True, text=True, timeout=300)
        
        return jsonify({
            'success': True,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
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
    app.run(host='0.0.0.0', port=5000, debug=True)
