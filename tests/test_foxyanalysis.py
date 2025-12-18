import pytest

from foxypack_telegram_telethon import FoxyTelegramAnalysis
from foxypack_telegram_telethon.answers import TelegramEnum


@pytest.mark.analysis
def test_telegram_public_post_link():
    analyzer = FoxyTelegramAnalysis()

    analysis = analyzer.get_analysis("https://t.me/telegram/1")
    analysis_two = analyzer.get_analysis("https://t.me/telegram/1")

    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://t.me/telegram/1"
    assert analysis.social_platform == "telegram"
    assert analysis.type_content == TelegramEnum.post.value
    assert analysis.code == "telegram/1"


@pytest.mark.analysis
def test_telegram_public_channel_link():
    analyzer = FoxyTelegramAnalysis()

    analysis = analyzer.get_analysis("https://t.me/telegram")
    analysis_two = analyzer.get_analysis("https://t.me/telegram")

    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://t.me/telegram"
    assert analysis.social_platform == "telegram"
    assert analysis.type_content == TelegramEnum.channel.value
    assert analysis.code == "telegram"

@pytest.mark.analysis
def test_telegram_private_channel_link():
    analyzer = FoxyTelegramAnalysis()

    analysis = analyzer.get_analysis("https://t.me/+abcdef")
    assert analysis.type_content == TelegramEnum.private_channel.value
    assert analysis.code == "abcdef"


@pytest.mark.analysis
def test_telegram_private_post_link():
    analyzer = FoxyTelegramAnalysis()

    analysis = analyzer.get_analysis("https://t.me/+abcdef/123")
    assert analysis.type_content == TelegramEnum.private_post.value
    assert analysis.code == "abcdef/123"
