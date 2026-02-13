#!/usr/bin/env python3
"""
OK Crisis Display App
Reads JSON files, displays content, no API keys needed
"""

from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def load_articles():
    """Load articles from JSON file."""
    try:
        if os.path.exists('data/articles.json'):
            with open('data/articles.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def load_comics():
    """Load comics from JSON file."""
    try:
        if os.path.exists('data/comics.json'):
            with open('data/comics.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return []

# Categories
CATEGORIES = {
    'world': {'name': 'World News'},
    'national': {'name': 'National News'},
    'business': {'name': 'Business & Finance'},
    'sports': {'name': 'Sports'},
    'entertainment': {'name': 'Entertainment'}
}

# Routes
@app.route('/')
def home():
    """Homepage with latest articles."""
    articles = load_articles()
    
    # Get latest 3 articles from each category
    latest_by_category = {}
    for category_key in CATEGORIES.keys():
        category_articles = [a for a in articles if a.get('category') == category_key]
        latest_by_category[category_key] = category_articles[:3]
    
    return render_template('display_index.html', 
                         categories=CATEGORIES,
                         latest_by_category=latest_by_category,
                         total_articles=len(articles))

@app.route('/category/<category_key>')
def category_page(category_key):
    """Category page with all articles."""
    if category_key not in CATEGORIES:
        return "Category not found", 404
    
    articles = load_articles()
    category_articles = [a for a in articles if a.get('category') == category_key]
    
    return render_template('display_category.html',
                         category_key=category_key,
                         category_name=CATEGORIES[category_key]['name'],
                         articles=category_articles)

@app.route('/article/<article_id>')
def article_detail(article_id):
    """Individual article page."""
    articles = load_articles()
    article = next((a for a in articles if a.get('id') == article_id), None)
    
    if not article:
        return "Article not found", 404
    
    return render_template('display_article.html', article=article)

@app.route('/comics')
def comics_page():
    """Comics page with all comic strips."""
    comics = load_comics()
    return render_template('display_comics.html', comics=comics)

@app.route('/comic/<comic_id>')
def comic_detail(comic_id):
    """Individual comic page."""
    comics = load_comics()
    comic = next((c for c in comics if c.get('id') == comic_id), None)
    
    if not comic:
        return "Comic not found", 404
    
    return render_template('display_comic_detail.html', comic=comic)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
