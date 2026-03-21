import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def end_with_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self.end_with_json(200, {"status": "Maverick AI is ready! ⚽️"})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAB1yiaZJGYsthdwqVezeWAP6pARvVLK04")
        
        # Using v1beta and gemini-1.5-flash-latest for maximum stability!
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        
        system_msg = data.get('system', '')
        user_msg = data.get('messages', [])[-1]['content'] if data.get('messages') else ""
        prompt = f"{system_msg}\n\nUser Instruction: {user_msg}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            res_json = res.json()
            
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
                self.end_with_json(200, {"content": [{"type": "text", "text": ai_text}]})
            else:
                error_message = res_json.get('error', {}).get('message', 'Google Brain Mismatch')
                self.end_with_json(200, {"content": [{"type": "text", "text": f"❌ Google Error: {error_message}"}]})
        except Exception as e:
            self.end_with_json(500, {"error": str(e)})


