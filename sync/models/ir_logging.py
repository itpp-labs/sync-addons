# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models

LOG_DEBUG = "debug"
LOG_INFO = "info"
LOG_WARNING = "warning"
LOG_ERROR = "error"
LOG_CRITICAL = "critical"

SHORT_MESSAGE_LINES = 5
SHORT_MESSAGE_CHARS = 100


class IrLogging(models.Model):
    _inherit = "ir.logging"

    sync_job_id = fields.Many2one("sync.job", ondelete="cascade")
    sync_task_id = fields.Many2one("sync.task", related="sync_job_id.task_id")
    sync_project_id = fields.Many2one(
        "sync.project", related="sync_job_id.task_id.project_id"
    )
    message_short = fields.Text(string="Message...", compute="_compute_message_short")
    type = fields.Selection(
        selection_add=[("data_out", "Data Transmission"), ("data_in", "Response")],
        ondelete={
            "data_out": lambda records: records.write({"type": "server"}),
            "data_in": lambda records: records.write({"type": "server"}),
        },
    )

    def _compute_message_short(self):
        for r in self:
            lines = r.message.split("\n")
            message_short = "\n".join(
                [
                    line[:SHORT_MESSAGE_CHARS] + "..."
                    if len(line) > SHORT_MESSAGE_CHARS
                    else line
                    for line in lines[:SHORT_MESSAGE_LINES]
                ]
            )
            if len(lines) > SHORT_MESSAGE_LINES:
                message_short += "\n..."
            r.message_short = message_short
