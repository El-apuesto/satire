import json
from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Store article in Vercel KV
        import os
        kv_url = os.environ.get('KV_URL')
        kv_rest_api_token = os.environ.get('KV_REST_API_TOKEN')
        kv_rest_api_read_only_token = os.environ.get('KV_REST_API_READ_ONLY_TOKEN')
        
        # Store article data
        article_key = f"article:{data.get('id', 'unknown')}"
        article_data = json.dumps(data)
        
        # Call Vercel KV API
        import requests
        response = requests.put(
            f"{kv_url}/kv/{article_key}",
            headers={
                "Authorization": f"Bearer {kv_rest_api_token}",
                "Content-Type": "application/json"
            },
            data=article_data
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "stored": True}).encode())
    
    def do_GET(self):
        # Get all articles from Vercel KV
        import os
        kv_url = os.environ.get('KV_URL')
        kv_rest_api_token = os.environ.get('KV_REST_API_TOKEN')
        
        import requests
        response = requests.get(
            f"{kv_url}/kv/article:*",
            headers={
                "Authorization": f"Bearer {kv_rest_api_token}",
                "Content-Type": "application/json"
            }
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.content)
