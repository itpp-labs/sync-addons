# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Telegram Integration""",
    "summary": """Telegram integration powered by Sync Studio""",
    "category": "Discuss",
    "images": ["images/sync_telegram.jpg"],
    "version": "14.0.3.2.2",
    "application": False,
    "author": "IT Projects Labs, Ilya Ilchenko",
    "support": "help@itpp.dev",
    "website": "https://github.com/itpp-labs/sync-addons",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync"],
    "external_dependencies": {"python": ["python-telegram-bot"], "bin": []},
    "data": [
        "data/sync_project_data.xml",
        "data/mail_sync_project_data.xml",
        "views/mail/assets.xml",
    ],
    "demo": [
        "data/sync_project_data_demo.xml",
    ],
    "qweb": [
        "static/src/mail/components/discuss_sidebar/discuss_sidebar.xml",
        "static/src/mail/components/discuss_sidebar_item/discuss_sidebar_item.xml",
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
