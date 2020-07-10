# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)

BUTTON_DATA = {"button_data_key": "button_data_value"}


class TestEval(TransactionCase):
    def print_last_logs(self, limit=1):
        logs = self.env["ir.logging"].search([], limit=limit)
        for lg in logs:
            _logger.debug("ir.logging: %s", [lg.name, lg.level, lg.message])

    def create_project_task(self, project_vals, task_vals):
        project = self.env["sync.project"].create(
            dict(
                **{
                    "name": "Project Eval Test",
                    "param_ids": [
                        (0, 0, {"key": "KEY1", "value": "VALUE1"}),
                        (0, 0, {"key": "KEY2", "value": "VALUE2"}),
                    ],
                    "secret_ids": [
                        (0, 0, {"key": "SECRET1", "value": "SECRETVALUE1"}),
                        (0, 0, {"key": "SECRET2", "value": "SECRETVALUE2"}),
                    ],
                },
                **project_vals
            )
        )

        task = (
            self.env["sync.task"]
            .create(
                dict(
                    **{
                        "name": "Task eval test",
                        "project_id": project.id,
                        "button_ids": [(0, 0, {"trigger_name": "BUTTON_EVAL_TEST"})],
                    },
                    **task_vals
                )
            )
            .with_context(new_cursor_logs=False)
        )
        return project, task

    def test_imports(self):
        """imports should be available in Protected Code only"""

        # legal way
        pvals = {
            "secret_code": "from odoo import tools",
            "common_code": "log('imported package in common_code: %s' % tools.config)",
        }
        tvals = {
            "code": "\n".join(
                [
                    "log('imported package in task code: %s' % tools.config)",
                    "def handle_button():",
                    "    pass",
                ]
            )
        }
        p, t = self.create_project_task(pvals, tvals)
        t.button_ids.ensure_one()
        t.button_ids.start()
        self.print_last_logs(2)

        # import in common_code
        pvals = {
            "secret_code": "x=2+2",
            "common_code": "from odoo import tools \n"
            "log('imported package in common_code: %s' % tools.config)",
        }
        tvals = {
            "code": "\n".join(
                [
                    "def handle_button():",
                    "    log('imported package in task code: %s' % tools.config)",
                ]
            )
        }
        with self.assertRaises(ValidationError):
            p, t = self.create_project_task(pvals, tvals)
            # t.button_ids.ensure_one()
            # t.button_ids.run()

        # import in task's code
        pvals = {
            "secret_code": "x=2+2",
            "common_code": "x=5",
        }
        tvals = {
            "code": "\n".join(
                [
                    "from odoo import tools",
                    "def handle_button():",
                    "    log('imported package in task code: %s' % tools.config)",
                ]
            )
        }
        with self.assertRaises(ValidationError):
            p, t = self.create_project_task(pvals, tvals)
            # t.button_ids.ensure_one()
            # t.button_ids.run()

    def test_secrets(self):
        """Secrets  should be available in Protected Code only"""

        pvals = {
            "secret_code": "\n".join(
                [
                    "import hashlib",
                    "def hash(data):",
                    "    return hashlib.sha224(data.encode('utf-8')).hexdigest()",
                    "xxx = hash(secrets.SECRET1)",
                ]
            ),
        }
        # legal way
        pvals["common_code"] = "log('xxx in common_code: %s' % xxx)"
        tvals = {
            "code": """
def handle_button():
    log('2+2=%s' % (2+2))
"""
        }
        p, t = self.create_project_task(pvals, tvals)
        t.button_ids.ensure_one()
        t.button_ids.start()
        self.print_last_logs(2)

        # using in common_code
        pvals["common_code"] = "xxx = hash(secrets.SECRET1)"
        tvals = {
            "code": """
def handle_button():
    log('xxx in task code: %s' % xxx)
"""
        }
        p, t = self.create_project_task(pvals, tvals)
        t.button_ids.ensure_one()
        with self.assertRaises(ValueError):
            t.button_ids.start()

        # using in task's code
        pvals["common_code"] = "log('xxx in common_code: %s' % xxx)"
        tvals = {
            "code": "\n".join(
                [
                    "def handle_button():",
                    "    xxx = hash(secrets.SECRET1)",
                    "    log('xxx in task code: %s' % xxx)",
                ]
            )
        }
        p, t = self.create_project_task(pvals, tvals)
        t.button_ids.ensure_one()
        with self.assertRaises(ValueError):
            t.button_ids.start()
