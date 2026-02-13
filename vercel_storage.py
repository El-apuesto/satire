import json
import os
from vercel_kv import KV

# Vercel KV storage
kv = KV()

def save_articles(articles):
    """Save articles to Vercel KV."""
    kv.set("articles", json.dumps(articles))

def load_articles():
    """Load articles from Vercel KV."""
    try:
        articles_json = kv.get("articles")
        return json.loads(articles_json) if articles_json else []
    except:
        return []

def save_comics(comics):
    """Save comics to Vercel KV."""
    kv.set("comics", json.dumps(comics))

def load_comics():
    """Load comics from Vercel KV."""
    try:
        comics_json = kv.get("comics")
        return json.loads(comics_json) if comics_json else []
    except:
        return []
