# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from odoo.tests.common import TransactionCase, at_install, post_install

_logger = logging.getLogger(__name__)


# Use the same tags as in base_automation module tests
@post_install(True)
@at_install(False)
class TestTriggerDB(TransactionCase):
    def setUp(self):
        super(TestTriggerDB, self).setUp()
        funcs = self.env["sync.link"]._get_eval_context()
        self.get_link = funcs["get_link"]

    def test_trigger_db(self):
        """Test handle_db created in sync_demo.xml"""

        # activate project
        self.env.ref("sync.test_project").active = True
        # trigger event
        partner = (
            self.env["res.partner"]
            .with_context(new_cursor_logs=False)
            .create({"name": "Test Partner Name"})
        )
        # check that handler is executed
        param = self.env.ref("sync.test_project_param")
        link = self.get_link(param.value, partner.id)
        self.assertTrue(link)
