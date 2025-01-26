import os
from typing import Dict 
from telegram import Bot
from telegram.constants import ParseMode
import asyncio

class TelegramAlert:
    def __init__(self):
        self.bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
    async def send_alert(self, pair_data: Dict):
        """Send formatted alert to Telegram"""
        message = (
            f"🚀 **New Meme Coin Alert**\n"
            f"• Pair: `{pair_data['baseToken']['symbol']}/{pair_data['quoteToken']['symbol']}`\n"
            f"• Chain: `{pair_data['chainId']}`\n"
            f"• Liquidity: `${pair_data['liquidity']['usd']:,.0f}`\n"
            f"• 1h Volume: `${pair_data['volume']['h1']:,.0f}`\n"
            f"• [View on DexScreener]({pair_data['url']})"
        )
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Telegram error: {str(e)}")