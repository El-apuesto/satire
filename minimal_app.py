from flask import Flask, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# Simple HTML template inline
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin - Working</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: Arial; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .btn { background: #ff6b6b; color: white; padding: 15px 30px; border: none; cursor: pointer; margin: 10px; }
        .status { background: #333; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .success { background: #4caf50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Admin Dashboard</h1>
        <div class="status success">✅ System Online</div>
        <div class="status">Articles: {{ articles|length }}</div>
        <div class="status">Last: {{ last_update }}</div>
        
        <h2>Actions</h2>
        <button class="btn" onclick="generateNews()">Generate News</button>
        <button class="btn" onclick="window.location.href='/'">View Site</button>
        
        <div id="result"></div>
    </div>
    
    <script>
        async function generateNews() {
            document.getElementById('result').innerHTML = 'Generating...';
            try {
                const response = await fetch('/generate_news');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<div class="status success">✅ ' + data.message + '</div>';
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    '<div class="status">❌ Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>
"""

HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LUXE News</title>
    <style>
        body { background: #0a0a0a; color: white; font-family: Georgia; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .article { background: #1a1a1a; margin: 20px 0; padding: 30px; border-radius: 8px; }
        h1 { font-size: 32px; margin-bottom: 10px; }
        .meta { color: #999; font-size: 14px; margin-bottom: 20px; }
        .btn { background: #ff6b6b; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LUXE News</h1>
        <button class="btn" onclick="window.location.href='/admin'">Admin</button>
        
        {% for article in articles %}
        <div class="article">
            <h2>{{ article.title }}</h2>
            <div class="meta">{{ article.byline }} | {{ article.published_at }}</div>
            <div>{{ article.content[:300] }}...</div>
        </div>
        {% endfor %}
        
        {% if not articles %}
        <div class="article">
            <h2>No articles yet</h2>
            <p>Click "Generate News" in admin to create content.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# In-memory storage
articles = []

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, articles=articles)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_TEMPLATE, articles=articles, last_update="Just now")

@app.route('/generate_news', methods=['GET'])
def generate_news():
    try:
        article = {
            'id': datetime.now().isoformat(),
            'title': 'Breaking: Local Man Discovers Weather Changes Seasonally',
            'byline': 'Staff Writer',
            'content': 'In a shocking development, local resident Barry Thompson reportedly noticed that weather tends to change with seasons. "It\'s cold in winter and warm in summer," Thompson stated from his porch. Scientists were baffled by the revelation.',
            'published_at': datetime.now().strftime('%Y-%m-%d')
        }
        
        articles.append(article)
        
        # Keep only last 10
        if len(articles) > 10:
            articles.pop(0)
        
        return jsonify({
            'success': True,
            'message': 'Generated 1 article successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
