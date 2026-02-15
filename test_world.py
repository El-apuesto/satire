import sys
sys.path.append('crisis-display')

from src.api.newsdata import NewsDataAPI

api = NewsDataAPI()

print("Testing world category:")
articles = api.fetch_latest_news(category='world', limit=3)
print(f'Found {len(articles)} articles')
for i, a in enumerate(articles):
    print(f'{i+1}. Category: {a["category"]}')
    print(f'   Title: {a["title"]}')
    print(f'   Content: {a["content"][:100]}...')
    print()
