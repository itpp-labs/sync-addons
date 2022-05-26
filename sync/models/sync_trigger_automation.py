# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SyncTriggerAutomation(models.Model):

    _name = "sync.trigger.automation"
    _inherit = ["sync.trigger.mixin", "sync.trigger.mixin.actions"]
    _description = "DB Trigger"
    _sync_handler = "handle_db"

    automation_id = fields.Many2one(
        "base.automation", delegate=True, required=True, ondelete="cascade"
    )

    def unlink(self):
        self.mapped("automation_id").unlink()
        self.mapped("action_server_id").unlink()
        return super().unlink()

    def start(self, records):
        if self.active:
            if not self.sync_task_id:
                # workaround for old deployments
                _logger.warning(
                    "Task was deleted, but there is still base.automation record for it: %s"
                    % self.automation_id
                )
                return

            self.sync_task_id.start(self, args=(records,), with_delay=True)

    def get_code(self):
        return (
            """
env["sync.trigger.automation"].browse(%s).sudo().start(records)
"""
            % self.id
        )

    @api.onchange("model_id")
    def onchange_model_id(self):
        self.model_name = self.model_id.model

    @api.onchange("trigger")
    def onchange_trigger(self):
        if self.trigger in ["on_create", "on_create_or_write", "on_unlink"]:
            self.filter_pre_domain = (
                self.trg_date_id
            ) = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger in ["on_write", "on_create_or_write"]:
            self.trg_date_id = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger == "on_time":
            self.filter_pre_domain = False
