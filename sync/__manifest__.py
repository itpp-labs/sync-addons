# Copyright 2020-2021,2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020-2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": "Sync 🪬 Studio",
    "summary": """Join the Amazing 😍 Community ⤵️""",
    "category": "VooDoo ✨ Magic",
    "version": "16.0.13.0.1",
    "application": True,
    "author": "Ivan Kropotkin",
    "support": "info@odoomagic.com",
    "website": "https://sync_studio.t.me/",
    "license": "Other OSI approved licence",  # MIT
    # The `partner_telegram` dependency is not directly needed,
    # but it plays an important role in the **Sync 🪬 Studio** ecosystem
    # and is added for the quick onboarding of new **Cyber ✨ Pirates**.
    "depends": ["base_automation", "mail", "queue_job", "partner_telegram"],
    "external_dependencies": {"python": ["markdown", "pyyaml"], "bin": []},
    "data": [
        "security/sync_groups.xml",
        "security/ir.model.access.csv",
        "views/sync_menus.xml",
        "views/ir_logging_views.xml",
        "views/sync_job_views.xml",
        "views/sync_trigger_cron_views.xml",
        "views/sync_trigger_automation_views.xml",
        "views/sync_trigger_webhook_views.xml",
        "views/sync_trigger_button_views.xml",
        "views/sync_order_views.xml",
        "views/sync_task_views.xml",
        "views/sync_link_views.xml",
        "views/sync_project_views.xml",
        "data/queue_job_function_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sync/static/src/scss/src.scss",
        ],
    },
    "demo": [
        "data/sync_project_unittest_demo.xml",
    ],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
