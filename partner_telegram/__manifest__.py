# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": "Telegram Contact Field",
    "summary": """Join the Amazing 😍 Community ⤵️""",
    "category": "VooDoo ✨ Magic",
    "version": "16.0.1.0.0",
    "author": "Ivan Kropotkin",
    "support": "info@odoomagic.com",
    "website": "https://sync_studio.t.me/",
    "license": "Other OSI approved licence",  # MIT
    "data": [
        "views/res_partner_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "partner_telegram/static/src/js/telegram_widget.js",
            "partner_telegram/static/src/xml/telegram_widget.xml",
            "partner_telegram/static/src/scss/telegram_widget.scss",
        ],
    },
    "installable": True,
}
