from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import json
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Configuration
UPLOAD_FOLDER = 'static/comics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ADMIN_PASSWORD = 'admin123'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Data files
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
COMICS_FILE = os.path.join(DATA_DIR, 'comics.json')
PROMPTS_FILE = os.path.join(DATA_DIR, 'comic_prompts.json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_comics():
    try:
        with open(COMICS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_comics(comics):
    with open(COMICS_FILE, 'w') as f:
        json.dump(comics, f, indent=2)

def load_prompts():
    try:
        with open(PROMPTS_FILE, 'r') as f:
            return json.load(f)
    except:
        # Default prompts
        default_prompts = [
            {
                "id": str(uuid.uuid4()),
                "text": "Politicians making ridiculous promises during election season",
                "active": True,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Tech companies announcing absurd new features nobody asked for",
                "active": True,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Struggles of remote work and video calls",
                "active": True,
                "created_at": datetime.now().isoformat()
            }
        ]
        save_prompts(default_prompts)
        return default_prompts

def save_prompts(prompts):
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(prompts, f, indent=2)

# Website class for compatibility
class Website:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.articles_file = os.path.join(self.data_dir, "articles.json")
        self.comics_file = COMICS_FILE
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self._init_data_files()
    
    def _init_data_files(self):
        """Initialize empty data files if they don't exist."""
        if not os.path.exists(self.articles_file):
            with open(self.articles_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.comics_file):
            with open(self.comics_file, 'w') as f:
                json.dump([], f)
    
    def load_articles(self):
        """Load articles from JSON file."""
        try:
            with open(self.articles_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def load_comics(self):
        """Load comics from JSON file."""
        try:
            with open(self.comics_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_comic(self, comic):
        """Save a comic to the JSON file."""
        comics = self.load_comics()
        comics.append(comic)
        
        # Keep only the most recent comics (configurable)
        comics = comics[-50:]  # Keep last 50 comics
        
        with open(self.comics_file, 'w') as f:
            json.dump(comics, f, indent=2)

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

@app.route('/debug_anthropic')
def debug_anthropic():
    """Debug Anthropic module contents."""
    try:
        import anthropic
        debug_info = {
            "anthropic_dir": dir(anthropic),
            "anthropic_version": getattr(anthropic, '__version__', 'unknown'),
            "anthropic_file": anthropic.__file__ if hasattr(anthropic, '__file__') else 'no file'
        }
        
        # Try to find what's available
        available_classes = []
        for name in dir(anthropic):
            obj = getattr(anthropic, name)
            if hasattr(obj, '__call__') and ('Client' in name or 'Anthropic' in name):
                available_classes.append({
                    "name": name,
                    "type": type(obj).__name__,
                    "doc": obj.__doc__[:100] if obj.__doc__ else 'no doc'
                })
        
        debug_info["available_classes"] = available_classes
        
        # Test Anthropic client
        try:
            if Config.GROQ_API_KEY:
                client = anthropic.Anthropic(api_key=Config.GROQ_API_KEY)
                debug_info["anthropic_client"] = True
        except Exception as e:
            debug_info["anthropic_error"] = str(e)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({"error": str(e), "type": type(e).__name__})

@app.route('/debug')
def debug():
    """Debug endpoint to check what's failing."""
    try:
        import sys
        import os
        from config.settings import Config
        
        # Force disable proxies before any imports
        os.environ['NO_PROXY'] = '*'
        os.environ['no_proxy'] = '*'
        os.environ['HTTP_PROXY'] = ''
        os.environ['HTTPS_PROXY'] = ''

        debug_info = {
            "python_version": sys.version,
            "working_dir": os.getcwd(),
            "env_vars": {
                "NEWSDATA_API_KEY": bool(os.getenv('NEWSDATA_API_KEY')),
                "GROQ_API_KEY": bool(os.getenv('GROQ_API_KEY')),
                "ANTHROPIC_API_KEY": bool(os.getenv('ANTHROPIC_API_KEY')),
                "PEXELS_API_KEY": bool(os.getenv('PEXELS_API_KEY')),
                "REPLICATE_API_TOKEN": bool(os.getenv('REPLICATE_API_TOKEN'))
            },
            "config_loaded": bool(Config),
            "groq_import": False,
            "groq_client": False
        }
        
        # Test Groq import
        try:
            from groq import Groq
            debug_info["groq_import"] = True
            
            # Monkey patch to remove proxies argument
            original_init = Groq.__init__
            def patched_init(self, *args, **kwargs):
                if 'proxies' in kwargs:
                    del kwargs['proxies']
                return original_init(self, *args, **kwargs)
            Groq.__init__ = patched_init
            
            # Test Groq client
            if Config.GROQ_API_KEY:
                client = Groq(api_key=Config.GROQ_API_KEY)
                debug_info["groq_client"] = True
        except Exception as e:
            debug_info["groq_error"] = str(e)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({"error": str(e), "type": type(e).__name__})

@app.route('/test')
def test():
    """Simple test endpoint."""
    return jsonify({"success": True, "message": "App is working!"})

@app.route('/test_env')
def test_env():
    """Test environment variables."""
    import os
    return jsonify({
        "newsdata": bool(os.getenv('NEWSDATA_API_KEY')),
        "groq": bool(os.getenv('GROQ_API_KEY')),
        "pexels": bool(os.getenv('PEXELS_API_KEY')),
        "replicate": bool(os.getenv('REPLICATE_API_TOKEN'))
    })

@app.route('/run_cycle')
def run_cycle():
    """Manually trigger a news generation cycle."""
    try:
        from src.schedulers.automation_scheduler import AutomationScheduler
        scheduler = AutomationScheduler()
        results = scheduler.run_cycle()
        return jsonify({
            "success": True,
            "message": f"Generated {len(results.get('articles', []))} articles and {len(results.get('comics', []))} comics",
            "results": results
        })
    except ImportError as e:
        logger.error(f"Import error in run_cycle: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Import error: {str(e)}. Missing dependencies."
        }), 500
    except Exception as e:
        logger.error(f"Generation error in run_cycle: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Generation error: {str(e)}"
        }), 500

@app.route('/test_news')
def test_news():
    """Test news fetching without full cycle."""
    try:
        from src.fetchers.news_fetcher import NewsFetcher
        fetcher = NewsFetcher()
        news_stories = fetcher.fetch_news()
        return jsonify({
            "success": True,
            "message": f"Fetched {len(news_stories)} news stories",
            "stories": news_stories[:3]  # First 3 stories
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"News fetch error: {str(e)}"
        }), 500

# Admin routes
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect password', 'error')
    
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    comics = load_comics()
    prompts = load_prompts()
    
    return render_template('admin_dashboard.html', comics=comics, prompts=prompts)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/upload_comic', methods=['POST'])
def upload_comic():
    """Upload a new comic."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    if 'comic_file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    
    file = request.files['comic_file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Create comic entry
        comic = {
            "id": str(uuid.uuid4()),
            "title": request.form.get('title', 'Untitled Comic'),
            "description": request.form.get('description', ''),
            "image_url": f"/static/comics/{unique_filename}",
            "panels": int(request.form.get('panels', 3)),
            "created_at": datetime.now().isoformat(),
            "is_manual": True
        }
        
        comics = load_comics()
        comics.insert(0, comic)  # Add to beginning
        save_comics(comics)
        
        return jsonify({"success": True, "comic": comic})
    
    return jsonify({"success": False, "error": "Invalid file type"}), 400

@app.route('/admin/delete_comic/<comic_id>', methods=['POST'])
def delete_comic(comic_id):
    """Delete a comic."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    comics = load_comics()
    comic_to_delete = None
    
    for i, comic in enumerate(comics):
        if comic['id'] == comic_id:
            comic_to_delete = comics.pop(i)
            break
    
    if comic_to_delete:
        # Delete file if it's a manual upload
        if comic_to_delete.get('is_manual') and comic_to_delete.get('image_url'):
            try:
                filepath = comic_to_delete['image_url'].lstrip('/')
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
        
        save_comics(comics)
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Comic not found"}), 404

@app.route('/admin/add_prompt', methods=['POST'])
def add_prompt():
    """Add a new AI comic prompt."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    prompt_text = request.form.get('prompt_text', '').strip()
    if not prompt_text:
        return jsonify({"success": False, "error": "Prompt text is required"}), 400
    
    prompt = {
        "id": str(uuid.uuid4()),
        "text": prompt_text,
        "active": True,
        "created_at": datetime.now().isoformat()
    }
    
    prompts = load_prompts()
    prompts.insert(0, prompt)
    save_prompts(prompts)
    
    return jsonify({"success": True, "prompt": prompt})

@app.route('/admin/toggle_prompt/<prompt_id>', methods=['POST'])
def toggle_prompt(prompt_id):
    """Toggle a prompt's active status."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    prompts = load_prompts()
    for prompt in prompts:
        if prompt['id'] == prompt_id:
            prompt['active'] = not prompt['active']
            save_prompts(prompts)
            return jsonify({"success": True, "active": prompt['active']})
    
    return jsonify({"success": False, "error": "Prompt not found"}), 404

@app.route('/admin/delete_prompt/<prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    """Delete a prompt."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    prompts = load_prompts()
    for i, prompt in enumerate(prompts):
        if prompt['id'] == prompt_id:
            prompts.pop(i)
            save_prompts(prompts)
            return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Prompt not found"}), 404

@app.route('/admin/generate_ai_comic', methods=['POST'])
def generate_ai_comic():
    """Generate an AI comic from a selected prompt."""
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 401
    
    prompt_id = request.form.get('prompt_id')
    if not prompt_id:
        return jsonify({"success": False, "error": "Prompt ID is required"}), 400
    
    prompts = load_prompts()
    selected_prompt = None
    
    for prompt in prompts:
        if prompt['id'] == prompt_id and prompt['active']:
            selected_prompt = prompt
            break
    
    if not selected_prompt:
        return jsonify({"success": False, "error": "Prompt not found or inactive"}), 404
    
    try:
        # Generate comic using the prompt
        from src.generators.comic_generator import ComicGenerator
        generator = ComicGenerator()
        
        # Create a mock article for the comic generator
        mock_article = {
            'title': selected_prompt['text'],
            'content': selected_prompt['text'],
            'category': 'custom'
        }
        
        comic_path = generator.generate_comic_strip(
            mock_article['title'],
            mock_article['content'],
            mock_article['category']
        )
        
        if comic_path:
            # Convert local path to web path
            web_path = comic_path.replace('\\', '/').lstrip('/')
            
            comic = {
                "id": str(uuid.uuid4()),
                "title": f"AI Comic: {selected_prompt['text'][:50]}...",
                "description": f"Generated from prompt: {selected_prompt['text']}",
                "image_url": f"/{web_path}",
                "panels": 3,
                "created_at": datetime.now().isoformat(),
                "is_manual": False,
                "prompt_id": prompt_id
            }
            
            comics = load_comics()
            comics.insert(0, comic)
            save_comics(comics)
            
            return jsonify({"success": True, "comic": comic})
        else:
            return jsonify({"success": False, "error": "Failed to generate comic"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
