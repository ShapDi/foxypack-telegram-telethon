from foxypack import AnswersAnalysis

from foxypack_telegram_telethon.answers import TelegramAnswersAnalysis


def as_telegram_analysis(
    analysis: AnswersAnalysis,
) -> TelegramAnswersAnalysis:
    if not isinstance(analysis, TelegramAnswersAnalysis):
        raise TypeError("Analysis is not TelegramAnswersAnalysis")

    return analysis
