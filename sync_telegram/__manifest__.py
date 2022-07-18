# Copyright 2020-2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Telegram Integration""",
    "summary": """Telegram integration powered by Sync Studio""",
    "category": "Discuss",
    "images": ["images/sync_telegram.jpg"],
    "version": "15.0.5.0.0",
    "application": False,
    "author": "IT Projects Labs, Ilya Ilchenko",
    "support": "help@itpp.dev",
    "website": "https://t.me/sync_studio",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "multi_livechat"],
    "external_dependencies": {"python": ["pyTelegramBotAPI"], "bin": []},
    "data": [
        "data/sync_project_context_data.xml",
        "data/sync_project_data.xml",
        "data/mail_sync_project_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/sync_telegram/static/src/models/discuss/discuss.js",
            "/sync_telegram/static/src/models/discuss_sidebar_category/discuss_sidebar_category.js",
        ],
    },
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
