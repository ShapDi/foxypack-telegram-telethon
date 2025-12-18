from foxy_entities import EntitiesController

from foxypack_telegram_telethon import (
    FoxyTelegramAnalysis,
    FoxyTelegramStat,
)


def test_account_entity(test_account):
    controller = EntitiesController()
    controller.add_entity(test_account)

    telegram_stat = FoxyTelegramStat(entities_controller=controller)
    telegram_stat_two = FoxyTelegramStat(entities_controller=controller)

    analysis = FoxyTelegramAnalysis().get_analysis(
        "https://t.me/howdyho_official/8585"
    )

    stat_one = telegram_stat.get_statistics(analysis)
    stat_two = telegram_stat_two.get_statistics(analysis)

    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.post_id == stat_two.post_id
    assert stat_one.text == stat_two.text
    assert stat_one.analysis_status == stat_two.analysis_status
