import requests
import time
import os
import http.server
import socketserver
import threading
import sys
import random

sys.stdout.reconfigure(line_buffering=True)

# --- SERVER FOR RENDER/PYTHONANYWHERE ---
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"COOKIES MESSENGER BOT IS LIVE")

def run_server():
    PORT = int(os.environ.get('PORT', 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server started at port {PORT}")
        httpd.serve_forever()

# --- MAIN MESSAGING LOGIC ---
def send_messages():
    # Files se data read karna (Aapki base64 logic ke mutabiq)
    try:
        with open('password.txt', 'r') as f: password = f.read().strip()
        with open('tokennum.txt', 'r') as f: cookies_list = [c.strip() for c in f.readlines() if c.strip()]
        with open('convo.txt', 'r') as f: convo_id = f.read().strip()
        with open('file.txt', 'r') as f: text_file_path = f.read().strip()
        with open(text_file_path, 'r') as f: messages = [m.strip() for m in f.readlines() if m.strip()]
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('time.txt', 'r') as f: speed = int(f.read().strip())
        
        num_cookies = len(cookies_list)
        num_messages = len(messages)
        print(f">> BOT STARTED WITH {num_cookies} COOKIES <<", flush=True)

        while True:
            for msg_index in range(num_messages):
                # Cookie selection (Round robin logic)
                cookie_index = msg_index % num_cookies
                current_cookie = cookies_list[cookie_index]
                msg = messages[msg_index]

                # HTTP Headers setup
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
                    'Cookie': current_cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://mbasic.facebook.com',
                    'Referer': f'https://mbasic.facebook.com/messages/read/?tid=cid.g.{convo_id}'
                }

                # Mbasic endpoint for cookies
                url = f"https://mbasic.facebook.com/messages/send/?icm=1"
                payload = {
                    'tids': f'cid.g.{convo_id}',
                    'body': f"{hater} {msg}",
                    'send': 'Send'
                }

                try:
                    response = requests.post(url, data=payload, headers=headers)
                    t = time.strftime("%Y-%m-%d %I:%M:%S %p")
                    
                    if response.status_code == 200:
                        print(f"[+] Msg {msg_index + 1} sent to Convo {convo_id} via Cookie {cookie_index + 1}")
                        print(f"    - Time: {t}")
                    else:
                        print(f"[x] Failed Msg {msg_index + 1} with Cookie {cookie_index + 1}")
                except Exception as e:
                    print(f"[!] Request Error: {e}")

                time.sleep(speed)
            
            print("\n[+] All messages sent. Restarting...\n")

    except Exception as e:
        print(f"FATAL ERROR: {e}", flush=True)

if __name__ == "__main__":
    # Server ko background thread mein chalayein
    threading.Thread(target=run_server, daemon=True).start()
    send_messages()
