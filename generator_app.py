#!/usr/bin/env python3
"""
OK Crisis Generator App
Runs locally, generates content, saves to JSON files
"""

import json
import os
import requests
from datetime import datetime
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY', '')
LIFETOON_API_KEY = os.getenv('LIFETOON_API_KEY', '')

# Categories
CATEGORIES = {
    'world': {'name': 'World News', 'newsdata_category': 'world'},
    'national': {'name': 'National News', 'newsdata_category': 'politics'},
    'business': {'name': 'Business & Finance', 'newsdata_category': 'business'},
    'sports': {'name': 'Sports', 'newsdata_category': 'sports'},
    'entertainment': {'name': 'Entertainment', 'newsdata_category': 'entertainment'}
}

# Comic characters
COMIC_CHARACTERS = {
    'skip_mcgee': {'name': 'Skip McGee', 'role': 'Reporter'},
    'dr_winklestein': {'name': 'Dr. Winklestein', 'role': 'Expert'},
    'bartholomew': {'name': 'Bartholomew Puddington', 'role': 'Official'},
    'mildred': {'name': 'Mildred Henderson', 'role': 'Citizen'}
}

def fetch_news(category_key):
    """Fetch news from NewsData API."""
    try:
        url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&category={CATEGORIES[category_key]['newsdata_category']}&language=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])[:4]  # Get 4 stories
    except Exception as e:
        print(f"Error fetching {category_key}: {e}")
    return []

def generate_satire(news_story):
    """Generate satirical rewrite using Groq."""
    try:
        prompt = f"""
Rewrite this news story in a deadpan, satirical style for OK Crisis:

Original: {news_story.get('title', '')} - {news_story.get('description', '')}

Requirements:
- Make it absurd but believable
- Use deadpan humor
- Keep it professional news tone
- 200-300 words
- Include fake quotes from experts

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
                'temperature': 0.8,
                'max_tokens': 600
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating satire: {e}")
    return None

def generate_comic_with_replicate(news_story):
    """Generate comic using Replicate API."""
    try:
        characters = list(COMIC_CHARACTERS.keys())
        selected_chars = random.sample(characters, min(3, len(characters)))
        
        # Generate dialogue
        dialogue_prompt = f"""
Create 3-panel comic dialogue based on: {news_story.get('title', '')}
Characters: {[COMIC_CHARACTERS[char]['name'] for char in selected_chars]}
Format: PANEL 1: [CHARACTER]: [dialogue]
"""
        
        dialogue_response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [{'role': 'user', 'content': dialogue_prompt}],
                'temperature': 0.8,
                'max_tokens': 400
            }
        )
        
        if dialogue_response.status_code == 200:
            dialogue = dialogue_response.json()['choices'][0]['message']['content']
            
            # Generate comic with Replicate
            try:
                import replicate
                client = replicate.Client(api_token=REPLICATE_API_TOKEN)
                
                output = client.run(
                    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
                    input={
                        "prompt": f"Comic strip about: {news_story.get('title', '')[:100]}",
                        "width": 600,
                        "height": 400,
                        "num_outputs": 1
                    }
                )
                
                return {
                    'dialogue': dialogue,
                    'image_url': output[0],
                    'characters': ', '.join([COMIC_CHARACTERS[char]['name'] for char in selected_chars])
                }
            except Exception as e:
                print(f"Replicate error: {e}")
                return None
                
    except Exception as e:
        print(f"Error generating comic: {e}")
    return None

def get_pexels_image(query):
    """Get image from Pexels API."""
    try:
        PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'your_pexels_key')
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['photos'][0]['src']['large']
    except:
        pass
    return "https://via.placeholder.com/400x300/cccccc/666666?text=News+Image"

def generate_content():
    """Generate all content for the day."""
    print("🚀 Starting OK Crisis Content Generation...")
    
    # Debug: Check API keys
    print(f"🔑 GROQ API Key: {GROQ_API_KEY[:10]}..." if GROQ_API_KEY else "❌ GROQ API Key: Missing")
    print(f"🔑 NewsData API Key: {NEWSDATA_API_KEY[:10]}..." if NEWSDATA_API_KEY else "❌ NewsData API Key: Missing")
    print(f"🔑 Replicate API Token: {REPLICATE_API_TOKEN[:10]}..." if REPLICATE_API_TOKEN else "❌ Replicate API Token: Missing")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Load existing content
    articles = []
    comics = []
    
    if os.path.exists('data/articles.json'):
        with open('data/articles.json', 'r') as f:
            articles = json.load(f)
    
    if os.path.exists('data/comics.json'):
        with open('data/comics.json', 'r') as f:
            comics = json.load(f)
    
    new_articles = []
    new_comics = []
    
    # Generate articles
    for category_key, category_info in CATEGORIES.items():
        print(f"📰 Generating {category_info['name']}...")
        news_stories = fetch_news(category_key)
        
        for i, story in enumerate(news_stories[:4]):
            satire_content = generate_satire(story)
            if satire_content:
                article = {
                    'id': f"{category_key}_{datetime.now().isoformat()}_{i}",
                    'title': story.get('title', 'Breaking News'),
                    'content': satire_content,
                    'category': category_key,
                    'category_name': category_info['name'],
                    'source': story.get('source_id', 'OK Crisis'),
                    'published_at': datetime.now().isoformat(),
                    'image_url': get_pexels_image(f"{category_key},breaking news")
                }
                new_articles.append(article)
    
    # Generate comics
    print("🎨 Generating Comics...")
    for category_key, category_info in CATEGORIES.items():
        news_stories = fetch_news(category_key)
        if news_stories:
            comic_data = generate_comic_with_replicate(news_stories[0])
            if comic_data:
                comic = {
                    'id': f"comic_{category_key}_{datetime.now().isoformat()}",
                    'title': f"{category_info['name']} Comic",
                    'image_url': comic_data['image_url'],
                    'dialogue': comic_data['dialogue'],
                    'characters': comic_data['characters'],
                    'created_at': datetime.now().isoformat()
                }
                new_comics.append(comic)
    
    # Save content
    all_articles = new_articles + articles
    all_comics = new_comics + comics
    
    # Keep only latest 100 of each
    all_articles = all_articles[:100]
    all_comics = all_comics[:50]
    
    with open('data/articles.json', 'w') as f:
        json.dump(all_articles, f, indent=2)
    
    with open('data/comics.json', 'w') as f:
        json.dump(all_comics, f, indent=2)
    
    print(f"✅ Generated {len(new_articles)} articles and {len(new_comics)} comics!")
    print(f"📁 Saved to data/articles.json and data/comics.json")
    
    return len(new_articles), len(new_comics)

if __name__ == "__main__":
    generate_content()
