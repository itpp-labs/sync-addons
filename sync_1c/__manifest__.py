# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """1c Integration""",
    "summary": """1c.ru integration powered by Sync Studio""",
    "category": "Localization",
    "images": [],
    "version": "12.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/12.0/sync_1c/",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "hr"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["data/sync_project_data.xml"],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
