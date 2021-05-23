# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Telegram Integration""",
    "summary": """Telegram integration powered by Sync Studio""",
    "category": "Discuss",
    "images": ["images/sync_telegram.jpg"],
    "version": "14.0.2.0.0",
    "application": False,
    "author": "IT Projects Labs, Ilya Ilchenko",
    "support": "help@itpp.dev",
    "website": "https://github.com/itpp-labs/sync-addons",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/sync_project_data.xml",
        "data/mail_sync_project_data.xml",
        "views/mail/assets.xml",
    ],
    "demo": [],
    "qweb": [
        "static/src/mail/components/discuss_sidebar/discuss_sidebar.xml",
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
