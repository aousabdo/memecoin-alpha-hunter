from dotenv import load_dotenv
load_dotenv("config/.env")

import os
import asyncio
from telegram import Bot

async def test_token():
    try:
        bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
        me = await bot.get_me()
        print(f"✅ Token valid! Bot username: @{me.username}")
        await bot.send_message(
            chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            text="✅ MemeCoinAlphaHunter test alert!"
        )
    except Exception as e:
        print(f"❌ Token error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_token())