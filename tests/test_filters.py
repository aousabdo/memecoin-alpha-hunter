import pytest
from datetime import datetime, timedelta
from alphahunter.analysis.filters import filter_new_pairs

def get_mock_pairs():
    current_time = datetime.now().timestamp() * 1000  # Current time in milliseconds
    hour_ago = current_time - (3600 * 1000)  # 1 hour ago
    
    return [
        {  # Should pass all filters
            'pairCreatedAt': hour_ago,
            'liquidity': {'usd': 60000},
            'fdv': 900000,
            'chainId': 'ethereum'
        },
        {  # Should fail liquidity check
            'pairCreatedAt': hour_ago,
            'liquidity': {'usd': 40000},
            'fdv': 900000,
            'chainId': 'solana'
        },
        {  # Should fail FDV check
            'pairCreatedAt': hour_ago,
            'liquidity': {'usd': 60000},
            'fdv': 2000000,
            'chainId': 'base'
        }
    ]

def test_filter_new_pairs():
    config = {
        'thresholds': {
            'max_age_hours': 24,
            'min_liquidity': 50000,
            'max_fdv': 1000000
        }
    }
    
    filtered = filter_new_pairs(get_mock_pairs(), config)
    
    # Should only keep the first pair
    assert len(filtered) == 1
    assert filtered[0]['chainId'] == 'ethereum'
    assert filtered[0]['liquidity']['usd'] == 60000