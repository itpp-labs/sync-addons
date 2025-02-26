# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
from odoo import api, fields, models


class SyncOrder(models.Model):
    _name = "sync.order"
    _description = "Sync Order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char("Title")
    body = fields.Text("Order")
    sync_project_id = fields.Many2one("sync.project", related="sync_task_id.project_id")
    sync_task_id = fields.Many2one(
        "sync.task",
        ondelete="cascade",
        required=True,
    )
    description = fields.Html(related="sync_task_id.sync_order_description")
    record_id = fields.Reference(
        string="Blackjack",
        selection="_selection_record_id",
        help="Optional extra information to perform this task",
    )

    partner_ids = fields.Many2many("res.partner", string="Partners")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Canceled"),
        ],
        default="draft",
    )

    @api.model
    def _selection_record_id(self):
        mm = self.sync_task_id.sync_order_model_id
        if not mm:
            return []
        return [(mm.model, mm.name)]

    def action_done(self):
        self.write({"state": "done"})

    def action_confirm(self):
        self.write({"state": "open"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_refresh(self):
        # Magic
        pass
