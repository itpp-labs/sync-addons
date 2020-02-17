# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Telegram Leads""",
    "summary": """Generate Leads out of messages forwarded in Telegram""",
    "category": "",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=12.0",
    "images": ['images/telegram.png'],
    "version": "12.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "sync@it-projects.info",
    "website": "https://apps.odoo.com/apps/modules/12.0/telegram_leads/",
    "license": "Other OSI approved licence",  # MIT
    "price": 50.00,
    "currency": "EUR",

    "depends": [
        "openapi",
        "crm"
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/utm_data.xml",
        "security/openapi.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": False,

    # "demo_title": "Telegram Bot: Leads",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "Generate Leads out of messages forwarded in Telegram",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
