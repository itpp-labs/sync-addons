# Copyright 2024-2025 Ivan Yelizariev <https://twitter.com/yelizariev>
from odoo import fields, models


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
    sync_job_id = fields.Many2one("sync.job")
    description = fields.Html(related="sync_task_id.sync_order_description")
    # DEPRECATED. Use line_ids.record_id instead
    record_id = fields.Reference(
        string="Blackjack",
        selection="_selection_record_id",
        help="Optional extra information to perform this task",
    )
    line_ids = fields.One2many(
        "sync.order.line", "sync_order_id", string="Linked Records"
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


class SyncOrderLine(models.Model):
    _name = "sync.order.line"
    _description = "Sync Order Records"

    sync_order_id = fields.Many2one("sync.order")
    record_id = fields.Reference(
        string="Linked Record",
        selection="_selection_record_id",
        help="Optional extra information to perform this task",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("error", "Failed"),
            ("cancel", "Canceled"),
        ],
        default="draft",
    )
    value = fields.Char("Extra Input")
    result = fields.Char("Result")

    def _selection_record_id(self):
        mm = self.sync_order_id.sync_task_id.sync_order_model_id
        if not mm:
            return []
        return [(mm.model, mm.name)]

    def action_done(self, msg=None):
        self.write({"state": "done"})
        if msg:
            self.write({"result": msg})

    def action_confirm(self, msg=None):
        self.write({"state": "open"})
        if msg:
            self.write({"result": msg})

    def action_error(self, msg=None):
        self.write({"state": "error"})
        if msg:
            self.write({"result": msg})

    def action_cancel(self, msg=None):
        self.write({"state": "cancel"})
        if msg:
            self.write({"result": msg})
