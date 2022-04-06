# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020-2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Sync Studio""",
    "summary": """Synchronize anything with anything: SystemX↔Odoo, Odoo1↔Odoo2, SystemX↔SystemY. ETL/ESB tool similar to OCA/connector, but more flexible""",
    "category": "Extra Tools",
    "images": ["images/sync-studio.jpg"],
    "version": "14.0.5.1.0",
    "application": True,
    "author": "IT Projects Labs, Ivan Yelizariev",
    "support": "help@itpp.dev",
    "website": "https://t.me/sync_studio",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base_automation", "mail", "queue_job"],
    "external_dependencies": {"python": [], "bin": []},
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
        "views/sync_task_views.xml",
        "views/sync_project_views.xml",
        "views/sync_link_views.xml",
        "wizard/sync_make_module_views.xml",
        "data/queue_job_function_data.xml",
        "data/sync_project_context.xml",
    ],
    "demo": [
        "data/sync_project_telegram_demo.xml",
        "data/sync_project_odoo2odoo_demo.xml",
        "data/sync_project_trello_github_demo.xml",
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
