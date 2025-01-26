import pytest
from unittest.mock import AsyncMock
from telegram import Update, User
from alphahunter.utils.user_analyzer import UserAnalyzer

@pytest.mark.asyncio
async def test_user_profile_generation():
    # Mock Telegram user
    mock_user = User(
        id=5792079267,
        first_name="Alex",
        last_name="A",
        is_bot=False,
        language_code="en"
    )
    
    # Mock Update object
    mock_update = AsyncMock(Update)
    mock_update.effective_user = mock_user
    
    # Generate profile
    profile = UserAnalyzer.generate_user_profile(mock_update)
    
    # Assertions
    assert "👤 User Profile" in profile
    assert "5792079267" in profile
    assert "Alex" in profile
    assert "A" in profile
    assert "en" in profile