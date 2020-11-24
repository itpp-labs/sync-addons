# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Pagadito Payment Acquirer""",
    "summary": """Integration with Pagadito.com payment service""",
    "category": "Website",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=10.0",
    "images": [],
    "version": "10.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "Other OSI approved licence",  # MIT
    # "price": 9.00,
    # "currency": "EUR",
    "depends": ["payment", "website_sale", "website_portal_sale"],
    "external_dependencies": {"python": ["urlparse", "zeep"], "bin": []},
    "data": [
        "views/payment_pagadito_templates.xml",
        "views/payment_acquirer_views.xml",
        "views/website_templates.xml",
        "views/report_templates.xml",
        "views/portal_templates.xml",
        "data/payment_acquirer_data.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
    # "demo_title": "Pagadito Payment Acquirer",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "Integration with Pagadito.com payment service",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
