# -*- coding: utf-8 -*-
# Copyright 2019-2020 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Outgoing Webhooks""",
    "summary": """Send webhook on Odoo events: when record is created/updated/deleted""",
    "category": "Extra Tools",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=10.0",
    "images": ["images/base_automation_webhook.png"],
    "version": "8.0.2.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://t.me/sync_studio",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base_action_rule"],
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
