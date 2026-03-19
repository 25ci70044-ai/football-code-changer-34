import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve your site's files correctly
        path = self.path
        if path == "/" or path == "/index.html":
            target, content_type = "index.html", "text/html"
        elif path.endswith(".js"):
            target, content_type = path.lstrip("/"), "application/javascript"
        elif path.endswith(".css"):
            target, content_type = path.lstrip("/"), "text/css"
        else:
            target, content_type = path.lstrip("/"), "text/plain"

        try:
            full_path = os.path.join(os.getcwd(), target)
            with open(full_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "Maverick AI is live ⚽️"}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # GEMINI API Key from Vercel Env Vars
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAB1yiaZJGYsthdwqVezeWAP6pARvVLK04")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_msg = data.get('system', '')
        messages = data.get('messages', [])
        user_msg = messages[-1]['content'] if messages else ""
        prompt = f"{system_msg}\n\nUser Instruction: {user_msg}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            ai_text = res.json()['candidates'][0]['content']['parts'][0]['text']
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"content": [{"type": "text", "text": ai_text}]}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
