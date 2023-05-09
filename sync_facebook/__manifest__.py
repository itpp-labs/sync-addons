# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Facebook Integration""",
    "summary": """Facebook Family of Apps integration powered by Sync Studio""",
    "category": "Marketing",
    "images": ["images/sync_facebook.jpg"],
    "version": "15.0.1.0.0",
    "application": False,
    "author": "IT Projects Labs, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/14.0/sync",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "crm"],
    "external_dependencies": {"python": ["facebook_business"], "bin": []},
    "data": [
        "data/sync_project_data.xml",
        "data/crm/sync_project_data.xml",
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
