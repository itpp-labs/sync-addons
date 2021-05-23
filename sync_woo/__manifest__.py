# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """WooCommerce Integration""",
    "summary": """Woo integration powered by Sync Studio""",
    "category": "eCommerce",
    "images": ["images/sync_woo.jpg"],
    "version": "12.0.1.0.0",
    "application": False,
    "author": "IT Projects Labs, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/12.0/sync",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "sale"],
    "external_dependencies": {"python": ["woocommerce"], "bin": []},
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
