# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models


class SyncTriggerButton(models.Model):

    _name = "sync.trigger.button"
    _inherit = "sync.trigger.mixin"
    _description = "Manual Trigger"
    _sync_handler = "handle_button"

    name = fields.Char("Description")
    sync_task_id = fields.Many2one("sync.task", name="Task", ondelete="cascade")
    sync_project_id = fields.Many2one(
        "sync.project", related="sync_task_id.project_id", readonly=True
    )
    active = fields.Boolean(default=True)

    def start_button(self):
        job, _result = self.start(raise_on_error=False)
        return {
            "name": "Job triggered by clicking Button",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sync.job",
            "res_id": job.id,
            "target": "self",
        }

    def start(self, raise_on_error=True):
        return self.sync_task_id.start(self, force=True, raise_on_error=raise_on_error)
