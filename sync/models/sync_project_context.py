# Copyright 2020,2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models

EVAL_CONTEXT_PREFIX = "_eval_context_"


class SyncProjectContext(models.Model):

    _name = "sync.project.context"
    _description = "Project Context"
    _rec_name = "display_name"

    # name is used to match an execution context method (e.g. trello_github -> _eval_context_trello_github)
    name = fields.Char("Name", required=True)
    display_name = fields.Char("Display name", required=True)
    description = fields.Text(compute="_compute_eval_context_description")

    _sql_constraints = [("name_uniq", "unique (name)", "Name must be unique.")]

    def _compute_eval_context_description(self):
        for r in self:
            method = r.get_eval_context_method()
            r.description = method.__doc__

    def get_eval_context_method(self):
        self.ensure_one()
        return getattr(self, EVAL_CONTEXT_PREFIX + self.name)
