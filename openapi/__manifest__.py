# -*- coding: utf-8 -*-
# Copyright 2018-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """REST API/OpenAPI/Swagger""",
    "summary": """API to integrate Odoo with whatever system you need""",
    "category": "",
    # "live_test_url": "",
    "images": ['images/openapi-swagger.png'],
    "version": "10.0.1.1.3",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "sync@it-projects.info",
    "website": "https://apps.odoo.com/apps/modules/10.0/openapi/",
    "license": "Other OSI approved licence",  # MIT
    "price": 180.00,
    "currency": "EUR",

    "depends": [
        "web_tour",
        "web_settings_dashboard",
        "report",
    ],
    "external_dependencies": {"python": ['bravado_core', 'swagger_spec_validator'], "bin": []},
    "data": [
        "security/openapi_security.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/openapi_view.xml",
        "views/res_users_view.xml",
        "views/ir_model_view.xml",
    ],
    "demo": [
        "views/assets_demo.xml",
        "views/tour_views.xml",
        "demo/openapi_demo.xml",
        "demo/openapi_security_demo.xml",
    ],
    "qweb": [
        "static/src/xml/dashboard.xml",
        # Сommented until we discuss it
        # "static/src/xml/configure_api_button.xml"
    ],

    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
