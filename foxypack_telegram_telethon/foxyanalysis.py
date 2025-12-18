import re
import urllib.parse
from typing_extensions import override

from foxypack import FoxyAnalysis, DenialAnalyticsException
from foxypack_telegram_telethon.answers import (
    TelegramAnswersAnalysis,
    TelegramEnum,
)


class FoxyTelegramAnalysis(FoxyAnalysis):
    @staticmethod
    def clean_link(link: str) -> str:
        parsed = urllib.parse.urlparse(link)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    @staticmethod
    def get_type_content(link: str) -> str | None:
        if re.match(r"https?://t\.me/(joinchat/|\+)[^/]+/\d+/?$", link):
            return TelegramEnum.private_post.value

        if re.match(r"https?://t\.me/(joinchat/|\+)[^/]+/?$", link):
            return TelegramEnum.private_channel.value

        if re.match(r"https?://t\.me/[^/]+/\d+/?$", link):
            return TelegramEnum.post.value

        if re.match(r"https?://t\.me/[^/]+/?$", link):
            return TelegramEnum.channel.value

        return None

    @staticmethod
    def get_code(link: str) -> str | None:
        m = re.match(r"https?://t\.me/(?:joinchat/|\+)([^/]+)/(\d+)", link)
        if m:
            return f"{m.group(1)}/{m.group(2)}"

        m = re.match(r"https?://t\.me/(?:joinchat/|\+)([^/]+)", link)
        if m:
            return m.group(1)

        m = re.match(r"https?://t\.me/([^/]+)(?:/(\d+))?", link)
        if not m:
            return None

        channel, post_id = m.group(1), m.group(2)
        return f"{channel}/{post_id}" if post_id else channel

    @override
    def get_analysis(self, url: str) -> TelegramAnswersAnalysis:
        type_content = self.get_type_content(url)
        if type_content is None:
            raise DenialAnalyticsException(url)

        return TelegramAnswersAnalysis(
            url=self.clean_link(url),
            social_platform="telegram",
            type_content=type_content,
            code=self.get_code(url),
        )
