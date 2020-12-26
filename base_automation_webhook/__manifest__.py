# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Outgoing Webhooks""",
    "summary": """Send webhook on Odoo events: when record is created/updated/deleted""",
    "category": "Extra Tools",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=13.0",
    "images": ["images/base_automation_webhook.png"],
    "version": "13.0.2.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/13.0/base_automation_webhook/",
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
    # "demo_title": "Outgoing Webhooks",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "{SHORT_DESCRIPTION_OF_THE_MODULE}",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
