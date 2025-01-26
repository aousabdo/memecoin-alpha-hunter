from typing import List, Dict
from typing import List, Dict  # Add this import
from datetime import datetime

def filter_pairs(pairs: List[Dict], config: Dict) -> List[Dict]:
    filtered = []
    current_time = datetime.now().timestamp() * 1000  # Milliseconds
    
    for pair in pairs:
        age_hours = (current_time - pair.get('pairCreatedAt', 0)) / (1000 * 3600)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        fdv = pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        volume_1h = pair.get('volume', {}).get('h1', 0)
        
        if all([
            age_hours <= config['thresholds']['max_age_hours'],
            liquidity >= config['thresholds']['min_liquidity'],
            fdv <= config['thresholds']['max_fdv'],
            volume_1h > (volume_24h / 24) * config['thresholds']['min_volume_spike']
        ]):
            filtered.append(pair)
            
    return filtered