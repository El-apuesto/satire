from flask import Flask, render_template, request, jsonify
import json
import os
import requests
from datetime import datetime, timedelta
import schedule
import random

app = Flask(__name__)

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY', '')

# Categories
CATEGORIES = {
    'world': {'name': 'World News', 'newsdata_category': 'world'},
    'national': {'name': 'National News', 'newsdata_category': 'politics'},
    'business': {'name': 'Business & Finance', 'newsdata_category': 'business'},
    'sports': {'name': 'Sports', 'newsdata_category': 'sports'},
    'entertainment': {'name': 'Entertainment', 'newsdata_category': 'entertainment'}
}

# Data storage
DATA_DIR = 'data'
ARTICLES_FILE = os.path.join(DATA_DIR, 'articles.json')

def ensure_data_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'w') as f:
            json.dump([], f)

def load_articles():
    """Load articles from JSON file."""
    try:
        with open(ARTICLES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_articles(articles):
    """Save articles to JSON file."""
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)

def fetch_news(category_key):
    """Fetch news for a specific category."""
    try:
        category = CATEGORIES[category_key]
        url = 'https://newsdata.io/api/1/news'
        params = {
            'apikey': NEWSDATA_API_KEY,
            'country': 'us',
            'category': category['newsdata_category'],
            'size': 5
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching {category_key} news: {e}")
    return []

def generate_satire_article(original_story):
    """Generate satirical article using Groq."""
    try:
        prompt = f"""
Rewrite this news story in a deadpan, satirical style like The Onion:

Title: {original_story.get('title', '')}
Content: {original_story.get('description', '')}

Requirements:
- Keep it factual but add subtle, absurd humor
- Use professional journalistic tone
- Make it sound like legitimate news
- 300-500 words
- Include fake quotes from experts
- End with a punchline

Article:
"""
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 800
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating satire: {e}")
    return None

# Comic characters (persistent)
COMIC_CHARACTERS = {
    'skip_mcgee': {'name': 'Skip McGee', 'role': 'Reporter', 'personality': 'Cynical veteran'},
    'dr_winklestein': {'name': 'Dr. Winklestein', 'role': 'Expert', 'personality': 'Academic fraud'},
    'bartholomew': {'name': 'Bartholomew Puddington', 'role': 'Official', 'personality': 'Bureaucratic nonsense'},
    'mildred': {'name': 'Mildred Henderson', 'role': 'Citizen', 'personality': 'Confused everyman'}
}

def generate_comic_dialogue(news_story):
    """Generate comic dialogue using persistent characters."""
    try:
        characters = list(COMIC_CHARACTERS.keys())
        selected_chars = random.sample(characters, min(3, len(characters)))
        
        prompt = f"""
Create a 3-panel comic strip dialogue based on this news story using these specific characters:

News Story: {news_story.get('title', '')} - {news_story.get('description', '')}

Characters to use:
{chr(10).join([f"- {COMIC_CHARACTERS[char]['name']} ({COMIC_CHARACTERS[char]['role']}): {COMIC_CHARACTERS[char]['personality']}" for char in selected_chars])}

Requirements:
- Create exactly 3 panels
- Use ONLY the characters listed above
- Each panel: PANEL [number]: [CHARACTER NAME]: [dialogue]
- Make it deadpan and satirical
- Reference the news situation ironically
- Keep dialogue short and punchy

PANEL 1:
[CHARACTER NAME]: [dialogue]

PANEL 2:
[CHARACTER NAME]: [dialogue]

PANEL 3:
[CHARACTER NAME]: [dialogue]
"""
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.8,
                'max_tokens': 600
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating comic: {e}")
    return None

def generate_comic_image(dialogue_text):
    """Generate comic strip image."""
    # For now, return a styled placeholder
    return "https://via.placeholder.com/600x400/1a1a1a/ffffff?text=Comic+Strip"

def get_article_image(article):
    """Get image for article from free sources."""
    # Try Unsplash first
    try:
        unsplash_url = f"https://source.unsplash.com/400x300/?{article['category']},news"
        return unsplash_url
    except:
        # Fallback to Pexels
        try:
            pexels_url = f"https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=400"
            return pexels_url
        except:
            # Final fallback
            return "https://via.placeholder.com/400x300/cccccc/666666?text=News+Image"

def generate_articles():
    """Generate articles for all categories."""
    articles = load_articles()
    new_articles = []
    
    for category_key, category_info in CATEGORIES.items():
        print(f"Fetching {category_info['name']}...")
        news_stories = fetch_news(category_key)
        
        # Generate 4 articles per category
        for i, story in enumerate(news_stories[:4]):
            print(f"Generating article {i+1}/4 for {category_info['name']}...")
            
            satire_content = generate_satire_article(story)
            if satire_content:
                article = {
                    'id': f"{category_key}_{datetime.now().isoformat()}_{i}",
                    'title': story.get('title', 'Breaking News'),
                    'content': satire_content,
                    'category': category_key,
                    'category_name': category_info['name'],
                    'source': story.get('source_id', 'Unknown'),
                    'published_at': datetime.now().isoformat(),
                    'original_title': story.get('title', ''),
                    'original_url': story.get('link', ''),
                    'image_url': get_article_image({'category': category_key})
                }
                new_articles.append(article)
    
    # Add new articles to existing ones
    all_articles = new_articles + articles
    
    # Keep only last 200 articles
    all_articles = all_articles[:200]
    
    save_articles(all_articles)
    return len(new_articles)

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
    
    return render_template('mvp_index.html', 
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
    
    return render_template('mvp_category.html',
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
    
    return render_template('mvp_article.html', article=article)

@app.route('/generate', methods=['POST'])
def generate_articles_route():
    """Manual article generation."""
    try:
        count = generate_articles()
        return jsonify({
            'success': True,
            'message': f'Generated {count} new articles!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/articles')
def api_articles():
    """API endpoint for articles."""
    articles = load_articles()
    return jsonify(articles)

# Scheduler
def scheduled_generation():
    """Run scheduled article generation."""
    print("Running scheduled article generation...")
    generate_articles()

def run_scheduler():
    """Run the scheduler in background."""
    schedule.every().day.at("08:00").do(scheduled_generation)
    schedule.every().day.at("20:00").do(scheduled_generation)
    
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

if __name__ == '__main__':
    ensure_data_dir()
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
