from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
import requests

app = Flask(__name__, template_folder='templates')

# Simple in-memory storage for Vercel
articles_storage = []
comics_storage = []

@app.route('/')
def home():
    """Home page with latest articles and comics."""
    return render_template('index.html', 
                         articles=articles_storage[:6], 
                         comics=comics_storage[:3])

@app.route('/articles')
def articles():
    """Articles page showing all articles."""
    return render_template('articles.html', articles=articles_storage)

@app.route('/comics')
def comics():
    """Comics page showing all comics."""
    return render_template('comics.html', comics=comics_storage)

@app.route('/admin')
def admin():
    """Admin dashboard."""
    # Add sample data for dashboard
    sample_prompts = [
        {"id": "1", "text": "Create a comic about technology fails", "active": True},
        {"id": "2", "text": "Political satire cartoon", "active": False}
    ]
    
    sample_comics = [
        {"id": "1", "title": "Tech Support Comic", "description": "When rebooting doesn't work", "created_at": "2024-02-12"}
    ]
    
    return render_template('simple_admin.html', articles=articles_storage, prompts=sample_prompts, comics=sample_comics)

@app.route('/run_cycle', methods=['GET'])
def run_cycle():
    """Simple news generation without file system dependencies."""
    try:
        # Generate sample article directly
        sample_article = {
            'id': datetime.now().isoformat(),
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
            'published_at': datetime.now().strftime('%Y-%m-%d'),
            'word_count': 156,
            'created_at': datetime.now().isoformat()
        }
        
        # Store in memory
        articles_storage.append(sample_article)
        
        # Keep only last 20 articles
        if len(articles_storage) > 20:
            articles_storage.pop(0)
        
        return jsonify({
            "success": True,
            "message": f"Generated 1 sample article",
            "results": {
                "articles": [sample_article],
                "comics": []
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Generation error: {str(e)}"
        }), 500

@app.route('/admin/upload_comic', methods=['POST'])
def upload_comic():
    """Handle comic upload - simplified for Vercel."""
    return jsonify({"success": True, "message": "Comic upload simulated"})

@app.route('/admin/add_prompt', methods=['POST'])
def add_prompt():
    """Handle prompt addition - simplified for Vercel."""
    return jsonify({"success": True, "message": "Prompt addition simulated"})

@app.route('/admin/toggle_prompt/<prompt_id>', methods=['POST'])
def toggle_prompt(prompt_id):
    """Handle prompt toggle - simplified for Vercel."""
    return jsonify({"success": True, "message": f"Prompt {prompt_id} toggled"})

@app.route('/admin/delete_prompt/<prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    """Handle prompt deletion - simplified for Vercel."""
    return jsonify({"success": True, "message": f"Prompt {prompt_id} deleted"})

@app.route('/admin/generate_ai_comic', methods=['POST'])
def generate_ai_comic():
    """Handle AI comic generation - simplified for Vercel."""
    return jsonify({"success": True, "message": "AI comic generation simulated"})

@app.route('/admin/delete_comic/<comic_id>', methods=['POST'])
def delete_comic(comic_id):
    """Handle comic deletion - simplified for Vercel."""
    return jsonify({"success": True, "message": f"Comic {comic_id} deleted"})

@app.route('/api/articles')
def api_articles():
    """API endpoint for articles."""
    return jsonify(articles_storage)

@app.route('/api/comics')
def api_comics():
    """API endpoint for comics."""
    return jsonify(comics_storage)

if __name__ == '__main__':
    app.run(debug=True)
