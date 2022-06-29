# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Multichannel Live Chat""",
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
    "demo": [],
    "qweb": [
        "static/src/components/discuss_sidebar/discuss_sidebar.xml",
        "static/src/components/discuss_sidebar_item/discuss_sidebar_item.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/multi_livechat/static/src/components/discuss_sidebar/discuss_sidebar.js",
            "/multi_livechat/static/src/models/messaging_initializer/messaging_initializer.js",
        ],
    },
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
