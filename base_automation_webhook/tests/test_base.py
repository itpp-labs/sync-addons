# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

from odoo.tests.common import TransactionCase, tagged


class TestAutomation(TransactionCase):
    @tagged("at_install", "post_install")
    def test_requests(self):
        """Check that requests package is available"""
        self.env["res.partner"].create({"name": "New Contact"})
