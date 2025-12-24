from foxy_entities import EntitiesController

from foxypack_telegram_telethon import (
    FoxyTelegramAnalysis,
    FoxyTelegramStat,
)


def test_get_statistics_public_post(test_account):
    controller = EntitiesController()
    controller.add_entity(test_account)

    stat = FoxyTelegramStat(entities_controller=controller)
    stat_two = FoxyTelegramStat(entities_controller=controller)

    analysis = FoxyTelegramAnalysis().get_analysis("https://t.me/howdyho_official/8585")

    stat_one = stat.get_statistics(analysis)
    stat_two_result = stat_two.get_statistics(analysis)

    assert stat_one.answer_id != stat_two_result.answer_id
    assert stat_one.post_id == stat_two_result.post_id
    assert stat_one.text == stat_two_result.text
    assert stat_one.analysis_status == stat_two_result.analysis_status


def test_get_statistics_public_channel(test_account):
    controller = EntitiesController()
    controller.add_entity(test_account)

    stat = FoxyTelegramStat(entities_controller=controller)
    stat_two = FoxyTelegramStat(entities_controller=controller)

    analysis = FoxyTelegramAnalysis().get_analysis("https://t.me/howdyho_official")

    stat_one = stat.get_statistics(analysis)
    stat_two_result = stat_two.get_statistics(analysis)

    assert stat_one.answer_id != stat_two_result.answer_id
    assert stat_one.channel_id == stat_two_result.channel_id
    assert stat_one.title == stat_two_result.title
    assert stat_one.analysis_status == stat_two_result.analysis_status
