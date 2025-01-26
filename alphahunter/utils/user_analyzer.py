from telegram import Update
from typing import Dict

class UserAnalyzer:
    @staticmethod
    def generate_user_profile(update: Update) -> str:
        user = update.effective_user
        return (
            "👤 User Profile\n"
            f" ├ ID: `{user.id}`\n"
            f" ├ Is Bot: `{user.is_bot}`\n"
            f" ├ First Name: `{user.first_name}`\n"
            f" ├ Last Name: `{user.last_name or 'None'}`\n"
            f" └ Language: `{user.language_code or 'Unknown'}`\n\n"
            "📊 Message Analysis Coming Soon!"
        )