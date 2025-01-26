# tests/get_chat_id.py
from dotenv import load_dotenv
load_dotenv("config/.env")

import os
import asyncio
from telegram import Bot

async def main():
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    updates = await bot.get_updates()
    if updates:
        print("Available chats:")
        for update in updates:
            print(f"- Chat ID: {update.message.chat.id} (Type: {update.message.chat.type})")
    else:
        print("No messages received yet. Send a message to your bot first.")

if __name__ == "__main__":
    asyncio.run(main())