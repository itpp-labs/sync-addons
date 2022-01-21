# Copyright 2021 Eugene Molotov <https://github.com/em234018>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """WhatsApp Integration""",
    "summary": """WhatsApp integration powered by Sync Studio and Chat API""",
    "category": "Marketing",
    "images": ["images/sync_whatsapp.jpg"],
    "version": "14.0.1.0.0",
    "application": False,
    "author": "IT Projects Labs, Eugene Molotov",
    "support": "help@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/14.0/sync",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "multi_livechat"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/sync_project_data.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
