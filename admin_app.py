from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

# Import the same Website class
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.website.app import Website

app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = 'your-secret-key-here'  # Change this for production

# Upload configuration
UPLOAD_FOLDER = 'static/comics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Custom prompts storage
PROMPTS_FILE = 'data/comic_prompts.json'

def load_prompts():
    """Load custom comic prompts."""
    try:
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create default prompts
            default_prompts = [
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Political Satire',
                    'prompt': 'Create a 3-panel comic about politicians making ridiculous promises during election season',
                    'active': True
                },
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Tech Industry',
                    'prompt': 'Create a 3-panel comic about tech companies announcing absurd new features nobody asked for',
                    'active': True
                },
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Everyday Life',
                    'prompt': 'Create a 3-panel comic about the struggles of remote work and video calls',
                    'active': False
                }
            ]
            save_prompts(default_prompts)
            return default_prompts
    except:
        return []

def save_prompts(prompts):
    """Save comic prompts to file."""
    os.makedirs('data', exist_ok=True)
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(prompts, f, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simple password protection (change this!)
ADMIN_PASSWORD = "admin123"

website = Website()

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
        else:
            flash('Invalid password')
            return redirect(url_for('admin_login'))
    
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST' and 'comic_file' in request.files:
        # Handle comic upload
        file = request.files['comic_file']
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)
            
            # Save comic data
            comic = {
                'id': str(uuid.uuid4()),
                'title': request.form.get('title', 'Untitled Comic'),
                'description': request.form.get('description', ''),
                'image_path': '/' + filepath.replace('\\', '/'),
                'created_at': datetime.now().isoformat(),
                'panels': request.form.get('panels', '3')
            }
            
            website.save_comic(comic)
            flash('Comic uploaded successfully!')
            return redirect(url_for('admin_dashboard'))
    
    # Load existing comics
    comics = website.load_comics()
    return render_template('admin_dashboard.html', comics=comics)

@app.route('/admin/delete/<comic_id>')
def delete_comic(comic_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    comics = website.load_comics()
    comics = [c for c in comics if c.get('id') != comic_id]
    
    # Save updated comics list
    with open(website.comics_file, 'w') as f:
        json.dump(comics, f, indent=2)
    
    flash('Comic deleted successfully!')
    return redirect(url_for('admin_dashboard'))

# Keep all existing routes
@app.route('/')
def home():
    """Home page with latest articles and comics."""
    articles = website.load_articles()
    comics = website.load_comics()
    
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
        <h1>LUXE Manual Cycle Trigger</h1>
        <p>Click the button below to run a news cycle:</p>
        <form method="GET" action="/run-cycle-now">
            <button type="submit">Run News Cycle</button>
        </form>
        '''
    
    try:
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
