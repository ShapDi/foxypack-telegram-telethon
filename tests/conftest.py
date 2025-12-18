import os
import pytest
from dotenv import load_dotenv

from foxypack_telegram_telethon import TelegramAccount


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def test_account():
    return TelegramAccount(
        api_id=int(os.getenv("TELEGRAM_API_ID")),
        api_hash=os.getenv("TELEGRAM_API_HASH"),
        session=os.getenv("TELEGRAM_SESSION"),
    )
