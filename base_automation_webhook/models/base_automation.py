# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import requests

# The file name is incorrect and should be called ir_actions_server.py instead
from odoo import api, models


class IrActionsServer(models.Model):

    _inherit = "ir.actions.server"

    @api.model
    def _get_eval_context(self, action=None):
        eval_context = super(IrActionsServer, self)._get_eval_context(action)

        def make_request(*args, **kwargs):
            return requests.request(*args, **kwargs)

        eval_context["make_request"] = make_request
        return eval_context
