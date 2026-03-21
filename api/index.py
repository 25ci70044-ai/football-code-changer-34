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
        self.end_with_json(200, {"status": "Maverick AI & Profile System is Live ⚽️"})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        path = self.path

        # --- 🔑 ROUTE: CHANGE PASSWORD ---
        if "/api/change-password" in path:
            username = data.get('username')
            new_pass = data.get('new_password')
            
            # Logic: We try to save to Redis (if connected)
            redis_url = os.environ.get("KV_REST_API_URL")
            redis_token = os.environ.get("KV_REST_API_TOKEN")
            
            if redis_url and redis_token:
                requests.get(f"{redis_url}/set/user:{username}:{new_pass}/active?_token={redis_token}")
                return self.end_with_json(200, {"status": "Permanent Save Success"})
            else:
                return self.end_with_json(200, {"status": "Success (Session only)"})

        # --- 🤖 ROUTE: MAVERICK AI (GEMINI 1.5 FLASH) ---
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAB1yiaZJGYsthdwqVezeWAP6pARvVLK04")
        
        # WE ARE KEEPING GEMINI 1.5 FLASH HERE:
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
                error_msg = res_json.get('error', {}).get('message', 'Gemini error')
                self.end_with_json(200, {"content": [{"type": "text", "text": f"❌ Google Error: {error_msg}"}]})
        except Exception as e:
            self.end_with_json(500, {"error": str(e)})
