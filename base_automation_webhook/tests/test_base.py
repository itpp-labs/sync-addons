# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestAutomation(TransactionCase):
    at_install = True
    post_install = True

    def test_requests(self):
        """Check that requests package is available"""
        self.env['res.partner'].create({'name': 'New Contact'})
