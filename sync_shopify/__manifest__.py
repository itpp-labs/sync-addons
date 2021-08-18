# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Shopify Integration""",
    "summary": """Shopify integration powered by Sync Studio""",
    "category": "eCommerce",
    "images": ["images/sync_shopify.jpg"],
    "version": "14.0.1.0.0",
    "application": False,
    "author": "IT Projects Labs, Eugene Molotov",
    "support": "help@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/14.0/sync_shopify",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync", "sale"],
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
