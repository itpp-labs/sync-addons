# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Sync Twindis""",
    "summary": """Twindis integration powered by Sync Studio""",
    "category": "Extra Tools",
    "images": ["images/sync_twindis.jpg"],
    "version": "14.0.1.0.0",
    "author": "IT Projects Labs, Denis Mudarisov",
    "support": "help@itpp.dev",
    "website": "https://github.com/itpp-labs/sync-addons",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sale_management", "sync", "purchase"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/sync_project_data.xml",
        "data/data.xml",
    ],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
