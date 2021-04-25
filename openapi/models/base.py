# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def search_or_create(self, vals, active_test=True):
        domain = [(k, "=", v) for k, v in vals.items()]
        records = self.with_context(active_test=active_test).search(domain)
        is_new = False
        if not records:
            is_new = True
            records = self.create(vals)
        return (is_new, records.ids)
