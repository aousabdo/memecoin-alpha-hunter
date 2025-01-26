from typing import List, Dict, Optional
import requests
import time

class DexScreenerClient:
    BASE_URL = "https://api.dexscreener.com/latest/dex"
    
    def __init__(self, rate_limit: int = 5):
        self.rate_limit = rate_limit
        self.last_call = 0.0
        
    def _rate_limit_sleep(self) -> None:
        elapsed = time.time() - self.last_call
        if elapsed < 1/self.rate_limit:
            time.sleep(1/self.rate_limit - elapsed)
        self.last_call = time.time()
        
    def get_new_pairs(self, chain: str) -> List[Dict]:
        self._rate_limit_sleep()
        try:
            response = requests.get(f"{self.BASE_URL}/search?q={chain}")
            response.raise_for_status()
            return response.json().get('pairs', [])
        except Exception as e:
            print(f"DexScreener API error: {str(e)}")
            return []
            
    def get_pair_details(self, chain_id: str, pair_address: str) -> Optional[Dict]:
        self._rate_limit_sleep()
        try:
            response = requests.get(f"{self.BASE_URL}/pairs/{chain_id}/{pair_address}")
            response.raise_for_status()
            return response.json().get('pairs', [{}])[0]
        except Exception as e:
            print(f"Pair details error: {str(e)}")
            return None