# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

# The file name is choosen in favor of model name in next odoo versions
from odoo import models, api
import requests


class IrActionsServer(models.Model):

    _inherit = 'ir.actions.server'

    @api.model
    def _get_eval_context(self, action=None):
        eval_context = super(IrActionsServer, self)._get_eval_context(action)
        eval_context['requests'] = requests
        return eval_context
