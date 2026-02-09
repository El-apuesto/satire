from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

# Flask app for PythonAnywhere deployment
app = Flask(__name__)

# Set template path to current directory
app.template_folder = 'templates'

# Import the same Website class used by automation
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.website.app import Website

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
        <p>Click the button below to run a news cycle:</p>
        <form method="GET" action="/run-cycle-now">
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

@app.route('/run-cycle-now')
def run_cycle_now():
    """Actually run the cycle."""
    import subprocess
    import json
    
    try:
        result = subprocess.run(['python', 'main.py', 'manual'], 
                              capture_output=True, text=True, timeout=300)
        
        return f'''
        <h1>News Cycle Complete!</h1>
        <h2>Output:</h2>
        <pre>{result.stdout}</pre>
        <a href="/run-cycle">Run Another Cycle</a>
        '''
    except Exception as e:
        return f'''
        <h1>Error Running Cycle</h1>
        <pre>{str(e)}</pre>
        <a href="/run-cycle">Try Again</a>
        '''

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
