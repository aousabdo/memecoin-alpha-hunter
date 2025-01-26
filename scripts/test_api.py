from alphahunter.data.dex_client import DexScreenerClient

def test_dex_connection():
    dex = DexScreenerClient()
    pairs = dex.search_pairs("ethereum")
    assert len(pairs) > 0
    print("API test passed! Found", len(pairs), "Ethereum pairs")

if __name__ == "__main__":
    test_dex_connection()