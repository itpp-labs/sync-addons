# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


def generate_ref():
    return str(uuid.uuid4())


class TestLink(TransactionCase):
    def setUp(self):
        super(TestLink, self).setUp()
        funcs = self.env["sync.link"]._get_eval_context()
        self.get_link = funcs["get_link"]
        self.set_link = funcs["set_link"]
        self.search_links = funcs["search_links"]

    def create_record(self):
        return self.env["res.partner"].create({"name": "Test"})

    def test_odoo_link(self):
        REL = "sync_test_links_partner"
        REL2 = "sync_test_links_partner2"

        self.assertFalse(self.env["res.partner"].search([]).search_links(REL))

        # Set and get links
        r = self.create_record()
        ref = generate_ref()
        r.set_link(REL, ref)
        glink = self.get_link(REL, ref)
        self.assertEqual(r, glink.odoo)
        self.assertEqual(ref, glink.external)
        glink = r.search_links(REL)
        self.assertEqual(r, glink.odoo)
        self.assertEqual(ref, glink.external)

        # check search_links
        all_links = self.env["res.partner"].search([]).search_links(REL)
        self.assertEqual(1, len(all_links))
        self.assertEqual(r, all_links[0].odoo)

        # update sync_date
        now = datetime.now() - relativedelta(days=1)
        all_links.update_links(now)
        glink = self.get_link(REL, ref)
        self.assertEqual(glink.sync_date, now)

        # update sync_date
        now = datetime.now()
        glink.update_links(now)
        glink = self.get_link(REL, ref)
        self.assertEqual(glink.sync_date, now)

        # check search_links
        all_links = self.env["res.partner"].search([]).search_links(REL)
        self.assertTrue(all_links)
        self.assertEqual(1, len(all_links))
        self.assertEqual(r, all_links[0].odoo)

        # Multiple refs for the same relation and record
        r = self.create_record()
        ref1 = generate_ref()
        ref2 = generate_ref()
        r.set_link(REL, ref1)
        with self.assertRaises(ValidationError):
            r.set_link(REL, ref2)
        r.set_link(REL, ref2, allow_many2many=True)

        # Multiple records for the same relation and ref
        r1 = self.create_record()
        r2 = self.create_record()
        ref = generate_ref()
        r1.set_link(REL, ref)
        with self.assertRaises(ValidationError):
            r2.set_link(REL, ref)
        r2.set_link(REL, ref, allow_many2many=True)

        # multiple links for different relation_name
        r = self.create_record()
        ref1 = generate_ref()
        r.set_link(REL, ref1)
        ref2 = generate_ref()
        r.set_link(REL2, ref2)
        self.assertFalse(self.get_link(REL2, ref1))

        # search links by two sets of references
        r1 = self.create_record()
        ref1 = generate_ref()
        r1.set_link(REL, ref1)
        r2 = self.create_record()
        ref2 = generate_ref()
        r2.set_link(REL, ref2)
        r3 = self.create_record()
        ref3 = generate_ref()
        r3.set_link(REL, ref3)
        r123 = r1 | r2 | r3
        links = r123.search_links(REL, [ref1, ref2])
        self.assertEqual(2, len(links))
        links = r123.search_links(REL, [ref1, ref2, ref3])
        self.assertEqual(3, len(links))
        r12 = r1 | r2
        links = r12.search_links(REL, [ref1, ref2, ref3])
        self.assertEqual(2, len(links))

        # check links
        all_links = self.env["res.partner"].search([]).search_links(REL)
        self.assertNotEqual(1, len(all_links))
        self.assertNotEqual(1, len(all_links.odoo))
        self.assertIsInstance(all_links.odoo.ids, list)
        self.assertIsInstance(all_links.external, list)
        self.assertIsInstance(all_links.sync_date, datetime)
        for link in all_links:
            self.assertIsInstance(link.odoo.id, int)

        # unlink
        all_links.unlink()
        all_links = self.env["res.partner"].search([]).search_links(REL)
        self.assertFalse(all_links)

    def test_external_link(self):
        REL = "sync_test_external_links"
        all_links = self.search_links(REL, {"github": None, "trello": None})
        self.assertFalse(all_links)

        # set get links
        now = datetime.now() - relativedelta(days=1)
        slink = self.set_link(REL, {"github": 1, "trello": 101}, sync_date=now)
        glink = self.get_link(REL, {"github": 1, "trello": 101})
        self.assertEqual(slink.get("github"), glink.get("github"))
        glink = self.get_link(REL, {"github": 1, "trello": None})
        self.assertEqual(slink.get("github"), glink.get("github"))
        glink = self.get_link(REL, {"github": None, "trello": 101})
        self.assertEqual(slink.get("github"), glink.get("github"))

        # update sync_date
        now = datetime.now()
        glink.update_links(now)
        glink = self.get_link(REL, {"github": None, "trello": 101})
        self.assertEqual(glink.sync_date, now)

        # search_links
        all_links = self.search_links(REL, {"github": None, "trello": None})
        self.assertEqual(1, len(all_links))
        self.assertEqual(now, all_links.sync_date)
        for link in all_links:
            self.assertEqual(now, link.sync_date)
        all_links.update_links(now)

        # sets operations
        self.set_link(REL, {"github": 2, "trello": 102})
        self.set_link(REL, {"github": 3, "trello": 103})
        self.set_link(REL, {"github": 4, "trello": 104})
        a = self.search_links(REL, {"github": [1, 2, 3], "trello": None})
        b = self.search_links(REL, {"github": None, "trello": [102, 103, 104]})
        self.assertNotEqual(a, b)
        self.assertEqual(set((a - b).get("trello")), {"101"})
        self.assertEqual(set((a - b).get("github")), {"1"})
        self.assertEqual(set((a | b).get("github")), {"1", "2", "3", "4"})
        self.assertEqual(set((a & b).get("github")), {"2", "3"})
        self.assertEqual(set((a ^ b).get("github")), {"1", "4"})

        # one2many
        self.set_link(REL, {"github": 5, "trello": 105})
        with self.assertRaises(Exception):
            self.set_link(REL, {"github": 5, "trello": 1005})
        self.set_link(REL, {"github": 5, "trello": 1005}, allow_many2many=True)
        with self.assertRaises(Exception):
            glink = self.get_link(REL, {"github": 5, "trello": None})
        glinks = self.search_links(REL, {"github": 5, "trello": None})
        self.assertEqual(2, len(glinks))
        glink1 = self.get_link(REL, {"github": 5, "trello": 105})
        glink2 = self.get_link(REL, {"github": 5, "trello": 1005})
        glink3 = self.get_link(REL, {"github": None, "trello": 105})
        glink4 = self.get_link(REL, {"github": None, "trello": 1005})
        self.assertEqual(glink1, glink3)
        self.assertEqual(glink2, glink4)
        self.assertNotEqual(glink1, glink2)
        elinks = self.search_links(REL, {"github": None, "trello": [105, 1005]})
        self.assertEqual(2, len(elinks))
        elinks = self.search_links(
            REL, {"github": [2, 5], "trello": [102, 100000002, 105, 1005]}
        )
        self.assertEqual(3, len(elinks))
        elinks = self.search_links(REL, {"github": [2, 5], "trello": None})
        self.assertEqual(3, len(elinks))

        # unlink
        all_links = self.search_links(REL, {"github": None, "trello": None})
        all_links.unlink()
        all_links = self.search_links(REL, {"github": None, "trello": None})
        self.assertFalse(all_links)
