# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Telegram Integration""",
    "summary": """Telegram integration powered by Sync Studio""",
    "category": "Discuss",
    "images": ["images/sync_telegram.png"],
    "version": "14.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ilya Ilchenko",
    "support": "help@itpp.dev",
    "website": "https://github.com/itpp-labs/sync-addons",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["data/sync_project_data.xml", "data/mail_sync_project_data.xml"],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
