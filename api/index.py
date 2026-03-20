import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve your home page correctly
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
        
        # CHANGED: Using v1 instead of v1beta
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_msg = data.get('system', '')
        messages = data.get('messages', [])
        user_msg = messages[-1]['content'] if messages else ""
        prompt = f"{system_msg}\n\nUser Instruction: {user_msg}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            res_json = res.json()
            
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"content": [{"type": "text", "text": ai_text}]}).encode())
            else:
                error_msg = res_json.get('error', {}).get('message', 'Gemini error')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"content": [{"type": "text", "text": f"❌ Google Error: {error_msg}"}]}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
