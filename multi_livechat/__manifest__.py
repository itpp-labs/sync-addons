# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Customer Chat""",
    "summary": """Be in touch with your partners via any supported channels (Telegram, WhatsApp, Instragram, etc.)""",
    "category": "Marketing",
    "images": ["images/multi_livechat.jpg"],
    "version": "15.0.1.2.0",
    "application": False,
    "author": "IT Projects Labs, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://t.me/sync_studio",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["mail"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/mail_channel_views.xml"],
    "demo": ["data/mail_channel_demo.xml", "data/base_automation_demo.xml"],
    "assets": {
        "web.assets_backend": [
            "multi_livechat/static/src/models/messaging_initializer/messaging_initializer.js",
            "multi_livechat/static/src/models/discuss/discuss.js",
            "multi_livechat/static/src/models/messaging_notification_handler/messaging_notification_handler.js",
            "multi_livechat/static/src/models/thread/thread.js",
            "multi_livechat/static/src/components/discuss/discuss.js",
            # demo
            "multi_livechat/static/src/demo/models/discuss/discuss.js",
            "multi_livechat/static/src/demo/models/discuss_sidebar_category/discuss_sidebar_category.js",
        ],
        "web.assets_qweb": [
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
