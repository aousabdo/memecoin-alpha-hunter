"""
Main analysis script for hunting alpha opportunities
"""
import yaml
from alphahunter.data.dex_client import DexScreenerClient
from alphahunter.analysis.filters import filter_new_pairs, detect_volume_spike
from alphahunter.alerts.telegram import TelegramAlert

def main():
    # Load config
    with open("../config/config.yml") as f:
        config = yaml.safe_load(f)
    
    # Initialize clients
    dex = DexScreenerClient()
    alert = TelegramAlert()
    
    # Find new pairs across chains
    all_pairs = []
    for chain in config['chains']:
        pairs = dex.search_pairs(chain)
        filtered = filter_new_pairs(pairs, config)
        all_pairs.extend(filtered)
    
    # Analyze and alert
    for pair in all_pairs:
        details = dex.get_pair_details(pair['chainId'], pair['pairAddress'])
        if detect_volume_spike(details):
            alert.send_alert("Volume spike detected", details)

if __name__ == "__main__":
    main()