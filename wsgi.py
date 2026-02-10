import sys
import os

# Add the project directory to the Python path
project_home = u'/home/yourusername/yourdomain.com'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import the Flask app
from src.website.app import app as application

# Set environment variables
os.environ['GROQ_API_KEY'] = 'your-groq-key-here'
os.environ['NEWSDATA_API_KEY'] = 'pub_39e106ccf96046c5bfe5d6dd1d9f6bed'
