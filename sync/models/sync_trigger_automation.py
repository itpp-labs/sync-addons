# Copyright 2020-2022,2025 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class BaseAutomationTriggerFix(models.Model):
    """Override _compute_trigger to preserve existing values.

    Odoo 18's base.automation._compute_trigger depends on model_id and
    unconditionally resets trigger to False.  This breaks programmatic
    creation/update where model_id and trigger are set together, because
    the ORM recomputation overrides the explicit value at flush time.

    The ORM invalidates the field cache before calling compute, so reading
    record.trigger inside compute returns the default (False) instead of
    the stored DB value.  We must read directly from the database.
    """

    _inherit = "base.automation"

    @api.depends("model_id")
    def _compute_trigger(self):
        # Read stored trigger values directly from DB — the ORM cache is
        # invalidated before compute runs, so record.trigger would return
        # False even when the DB holds a valid value.
        stored = {}
        existing = self.filtered("id")
        if existing:
            self.env.cr.execute(
                "SELECT id, trigger FROM base_automation WHERE id IN %s",
                [tuple(existing.ids)],
            )
            stored = dict(self.env.cr.fetchall())
        for record in self:
            record.trigger = stored.get(record.id) or False


class SyncTriggerAutomation(models.Model):

    _name = "sync.trigger.automation"
    _inherit = ["sync.trigger.mixin"]
    _description = "DB Trigger"
    _sync_handler = "handle_db"

    # DELEGATE=TRUE
    automation_id = fields.Many2one(
        "base.automation", delegate=True, required=True, ondelete="cascade"
    )
    sync_task_id = fields.Many2one("sync.task")
    sync_project_id = fields.Many2one(
        "sync.project", related="sync_task_id.project_id", readonly=True
    )

    def unlink(self):
        actions = self.action_server_ids
        automations = self.automation_id
        super().unlink()
        automations.unlink()
        actions.unlink()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for r in records:
            r.action_server_ids = [
                (
                    0,
                    0,
                    {
                        "name": r.trigger_name,
                        "state": "code",
                        "code": r.get_code(),
                        "model_id": r.automation_id.model_id.id,
                    },
                )
            ]
        return records

    def start(self, records):
        if self.active:
            sync_job = self.sync_task_id.start(self, args=(records,), with_delay=True)
            if records._name == "sync.order":
                records.write({"sync_job_id": sync_job.id})

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
        # TODO
        if self.trigger in ["on_create", "on_create_or_write", "on_unlink"]:
            self.filter_pre_domain = (
                self.trg_date_id
            ) = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger in ["on_write", "on_create_or_write"]:
            self.trg_date_id = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger == "on_time":
            self.filter_pre_domain = False
