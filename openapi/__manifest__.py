# Copyright 2018-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """REST API/OpenAPI/Swagger""",
    "summary": """API to integrate Odoo with whatever system you need""",
    "category": "",
    # "live_test_url": "",
    "images": ['images/openapi-swagger.png'],
    "version": "13.0.1.1.6",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "sync@it-projects.info",
    "website": "https://apps.odoo.com/apps/modules/13.0/openapi/",
    "license": "LGPL-3",
    "price": 180.00,
    "currency": "EUR",

    "depends": [
        "mail",
    ],
    "external_dependencies": {"python": ['bravado_core', 'swagger_spec_validator'], "bin": []},
    "data": [
        "security/openapi_security.xml",
        "security/ir.model.access.csv",
        "security/res_users_token.xml",
        # Сommented until we discuss it
        # "views/assets.xml",
        "views/openapi_view.xml",
        "views/res_users_view.xml",
        "views/ir_model_view.xml",
    ],
    "demo": [
        "demo/openapi_demo.xml",
        "demo/openapi_security_demo.xml",
    ],
    "qweb": [
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
