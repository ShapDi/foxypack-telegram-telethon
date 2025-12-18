from foxy_entities import SocialMediaEntity


class TelegramAccount(SocialMediaEntity):
    api_id: int
    api_hash: str
    session: str
