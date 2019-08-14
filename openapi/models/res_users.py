# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import uuid

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    namespace_ids = fields.Many2many('openapi.namespace', string='Allowed Integrations')
    token = fields.Char('Identification token',
                        default=lambda self: self._get_unique_token(),
                        required=True, copy=False, help='Authentication token for access to API (/api).')

    @api.multi
    def reset_token(self):
        for record in self:
            record.write({'token': self._get_unique_token()})

    def _get_unique_token(self):
        token = str(uuid.uuid4())
        while self.search_count([('token', '=', token)]):
            token = str(uuid.uuid4())
        return token

    @api.model
    def reset_all_tokens(self):
        self.search([]).reset_token()
