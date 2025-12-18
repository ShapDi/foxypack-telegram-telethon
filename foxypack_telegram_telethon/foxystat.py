import asyncio

from foxy_entities import EntitiesController
from foxy_entities.exceptions import PresenceObjectException
from foxypack import (
    FoxyStat,
    InternalCollectionException,
    AnswersAnalysis,
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel, Message
from typing_extensions import override

from foxypack_telegram_telethon.answers import (
    TelegramEnum,
    TelegramChannelAnswersStatistics,
    TelegramPostAnswersStatistics,
)
from foxypack_telegram_telethon.entities import TelegramAccount


class FoxyTelegramStat(FoxyStat):
    def __init__(self, entities_controller: EntitiesController | None = None):
        self._entities_controller = entities_controller

    @override
    def get_statistics(self, analysis: AnswersAnalysis):
        return asyncio.run(self._get_statistics_async_internal(analysis))

    @override
    async def get_statistics_async(self, analysis: AnswersAnalysis):
        return await self._get_statistics_async_internal(analysis)

    def _get_account(self) -> TelegramAccount:
        if self._entities_controller is None:
            raise InternalCollectionException
        try:
            return self._entities_controller.get_entity(TelegramAccount)
        except PresenceObjectException:
            raise InternalCollectionException

    async def _get_client(self) -> TelegramClient:
        account = self._get_account()

        client = TelegramClient(
            StringSession(account.session),
            account.api_id,
            account.api_hash,
        )

        await client.start()
        self._entities_controller.add_entity(account)
        return client

    @staticmethod
    async def _channel_from_entity(
        client: TelegramClient,
        channel: Channel,
        analysis: AnswersAnalysis,
    ) -> TelegramChannelAnswersStatistics:

        full = await client(GetFullChannelRequest(channel))

        return TelegramChannelAnswersStatistics(
            title=channel.title,
            channel_id=channel.id,
            username=channel.username,
            description=full.full_chat.about,
            subscribers=full.full_chat.participants_count,
            verified=channel.verified,
            creation_date=None,
            system_id=str(channel.id),
            analysis_status=analysis,
        )

    @staticmethod
    def _post_from_message(message: Message, channel: Channel, analysis: AnswersAnalysis):
        return TelegramPostAnswersStatistics(
            title=(message.message or "")[:50],
            post_id=message.id,
            channel_id=channel.id,
            channel_username=channel.username,
            text=message.message,
            views=message.views,
            forwards=message.forwards,
            replies=message.replies.replies if message.replies else None,
            publish_date=message.date.date() if message.date else None,
            system_id=str(message.id),
            analysis_status=analysis,
        )

    @staticmethod
    async def _resolve_private_channel(
            client: TelegramClient, invite_hash: str
    ):
        result = await client(ImportChatInviteRequest(invite_hash))
        return result.chats[0]

    async def _get_statistics_async_internal(
            self, analysis: AnswersAnalysis
    ):
        if analysis.social_platform != "telegram":
            raise InternalCollectionException

        client = await self._get_client()

        if analysis.type_content == TelegramEnum.channel.value:
            channel = await client.get_entity(analysis.code)
            return await self._channel_from_entity(client, channel, analysis)

        if analysis.type_content == TelegramEnum.post.value:
            channel_name, post_id = analysis.code.split("/")
            channel = await client.get_entity(channel_name)
            message = await client.get_messages(channel, ids=int(post_id))
            return self._post_from_message(message, channel, analysis)

        if analysis.type_content == TelegramEnum.private_channel.value:
            channel = await self._resolve_private_channel(client, analysis.code)
            return await self._channel_from_entity(client, channel, analysis)

        if analysis.type_content == TelegramEnum.private_post.value:
            invite_hash, post_id = analysis.code.split("/")
            channel = await self._resolve_private_channel(client, invite_hash)
            message = await client.get_messages(channel, ids=int(post_id))
            return self._post_from_message(message, channel, analysis)

        raise InternalCollectionException
