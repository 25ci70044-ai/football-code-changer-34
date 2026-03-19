# c:\Users\USER\.gemini\antigravity\scratch\football code changer\api\index.py
import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ... (keep the GET logic as it is for the home page)
        pass

    def do_POST(self):
        # Updated AI logic with detailed error reporting
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAB1yiaZJGYsthdwqVezeWAP6pARvVLK04")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_msg = data.get('system', '')
        messages = data.get('messages', [])
        user_msg = messages[-1]['content'] if messages else ""
        prompt = f"{system_msg}\n\nUser Instruction: {user_msg}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            res_json = res.json()
            
            # Check if Gemini returned a successful response
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"content": [{"type": "text", "text": ai_text}]}).encode())
            else:
                # If Gemini returned an error (like invalid key), tell the user exactly what it is
                error_message = res_json.get('error', {}).get('message', 'Unknown Gemini Error')
                self.send_response(200) # Send 200 so the UI can show the text
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"content": [{"type": "text", "text": f"❌ Error from Google: {error_message}"}]}).encode())
                
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"content": [{"type": "text", "text": f"❌ Connection Error: {str(e)}"}]}).encode())

