import sys
sys.path.append('crisis-display')

from src.api.newsdata import NewsDataAPI

api = NewsDataAPI()

print("Testing world category:")
articles = api.fetch_latest_news(category='world', limit=5)
print(f'Found {len(articles)} articles')
for a in articles[:3]:
    print(f'- {a["category"]}: {a["title"][:50]}...')

print("\nTesting business category:")
articles = api.fetch_latest_news(category='business', limit=5)
print(f'Found {len(articles)} articles')
for a in articles[:3]:
    print(f'- {a["category"]}: {a["title"][:50]}...')
