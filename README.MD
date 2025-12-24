# foxypack-telegram-telethon

Telegram integration module for **FoxyPack** based on **Telethon**.

Provides link analysis and statistics collection for Telegram channels and posts, including private content.

---

## Basic usage

### Analyze Telegram links

Add a module to the FoxyPack controller for analyzing Telegram links.

```python
from foxypack import FoxyPack
from foxypack_telegram_telethon import FoxyTelegramAnalysis

parser = FoxyPack().with_foxy_analysis(
    FoxyTelegramAnalysis()
)

parser.get_analysis("https://t.me/telegram/1")
```

### Collect statistics

Add a module to the FoxyPack controller for analyzing Telegram links.

```python
from foxy_entities import EntitiesController
from foxypack import FoxyPack
from foxypack_telegram_telethon import (
    TelegramAccount,
    FoxyTelegramStat,
)

account = TelegramAccount(
    api_id=123456,
    api_hash="your_api_hash",
    session="your_telethon_string_session",
)

controller = EntitiesController()
controller.add_entity(account)

parser = FoxyPack().with_foxy_stat(
    FoxyTelegramStat(entities_controller=controller)
)

parser.get_statistics("https://t.me/telegram/1")
```

### Supported links

* Public channels
* Public posts
* Private channels (invite links)
* Private posts (invite links)

### Supported content types

* channel
* post
* private_channel
* private_post
