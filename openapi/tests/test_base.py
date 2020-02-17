# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', 'at_install')
class TestBase(TransactionCase):

    def test_search_or_create(self):
        MODEL = 'res.partner'
        FIELD = 'name'
        VALUE = 'test_search_or_create'
        d = {FIELD: VALUE}
        self.env[MODEL].search([(FIELD, '=', VALUE)]).unlink()
        is_new, record_ids = self.env[MODEL].search_or_create(d.copy())
        record = self.env[MODEL].browse(record_ids)
        self.assertTrue(is_new)
        self.assertEqual(getattr(record, FIELD), VALUE)
        is_new, record_ids2 = self.env[MODEL].search_or_create(d.copy())
        record = self.env[MODEL].browse(record_ids2)
        self.assertFalse(is_new)
        self.assertEqual(record_ids[0], record_ids2[0])
