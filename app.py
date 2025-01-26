from gevent import monkey
monkey.patch_all(ssl=False)

import yaml
from prometheus_client import start_http_server, Counter
from alphahunter.data.dex_client import DexScreenerClient
from alphahunter.analysis.filters import filter_pairs
from alphahunter.alerts.telegram import TelegramAlert
import threading
import time
import os
from typing import Dict, List

from dotenv import load_dotenv
load_dotenv("config/.env")

# ======================
# Metrics & Monitoring
# ======================
ALERTS_SENT = Counter('alerts_sent', 'Number of alerts sent')
SCAN_ERRORS = Counter('scan_errors', 'Number of scan errors')
start_http_server(8001)

# ======================
# Configuration
# ======================
with open("config/config.yml") as f:
    config = yaml.safe_load(f)

# ======================
# Core Services
# ======================
dex = DexScreenerClient(rate_limit=10)
alert = TelegramAlert()

def scan_pairs():
    """Main scanning logic"""
    while True:
        try:
            all_pairs = []
            for chain in config['chains']:
                pairs = dex.get_new_pairs(chain)
                filtered = filter_pairs(pairs, config)
                all_pairs.extend(filtered)
                
            for pair in all_pairs:
                asyncio.run(alert.send_alert(pair))
                ALERTS_SENT.inc()
                
        except Exception as e:
            print(f"Scan error: {str(e)}")
            SCAN_ERRORS.inc()
        finally:
            time.sleep(config['scan_interval'])

# ======================
# Web Server
# ======================
def wsgi_app(environ, start_response):
    if environ['PATH_INFO'] == '/health':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found']

# ======================
# Execution
# ======================
if __name__ == "__main__":
    # Start scanner thread
    scanner_thread = threading.Thread(target=scan_pairs, daemon=True)
    scanner_thread.start()
    
    # Start web server
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()