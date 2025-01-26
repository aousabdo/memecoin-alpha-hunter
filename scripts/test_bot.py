from alphahunter.alerts.telegram import TelegramAlert
from dotenv import load_dotenv
import asyncio

load_dotenv("config/.env")

async def test_bot():
    alert = TelegramAlert()
    test_data = {
        "baseToken": {"symbol": "TEST"},
        "quoteToken": {"symbol": "USD"},
        "chainId": "testnet",
        "liquidity": {"usd": 100000},
        "url": "https://dexscreener.com/"
    }
    await alert.send_alert_async("Test alert", test_data)
    print("Check Telegram for test alert!")

if __name__ == "__main__":
    asyncio.run(test_bot())