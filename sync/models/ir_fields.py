# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    sync_project_id = fields.Many2one(
        "sync.project",
        string="Sync Project",
    )
