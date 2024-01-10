# Copyright 2021-2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Customer Chat""",
    "summary": """Be in touch with your partners via any supported channels (Telegram, WhatsApp, Instragram, etc.)""",
    "category": "Marketing",
    "images": ["images/multi_livechat.jpg"],
    "version": "16.0.2.0.0",
    "application": False,
    "author": "IT Projects Labs, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://itpp.dev/",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["mail"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/mail_channel_views.xml"],
    "demo": ["data/mail_channel_demo.xml", "data/base_automation_demo.xml"],
    "assets": {
        "web.assets_backend": [
            "multi_livechat/static/src/models/channel.js",
            "multi_livechat/static/src/models/discuss.js",
            "multi_livechat/static/src/models/thread.js",
            "multi_livechat/static/src/models/messaging.js",
            # demo
            "multi_livechat/static/src/demo/models/discuss.js",
            "multi_livechat/static/src/demo/models/discuss_sidebar_category.js",
            "multi_livechat/static/src/demo/models/res_users_settings.js",
            "multi_livechat/static/src/components/discuss_sidebar/discuss_sidebar.xml",
        ],
    },
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
