# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Outgoing Webhooks""",
    "summary": """Send webhook on Odoo events: when record is created/updated/deleted""",
    "category": "Extra Tools",
    "images": ["images/base_automation_webhook.png"],
    "version": "16.0.2.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base_automation"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [],
    "demo": ["data/base_automation_demo.xml"],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
