# Copyright 2019,2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2019 Anvar Kildebekov <https://it-projects.info/team/fedoranvar>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

prefix = "__base_api__."


@tagged("post_install", "at_install")
class TestBase(TransactionCase):
    def test_search_or_create(self):
        # define test variables
        partner_obj = self.env["res.partner"]
        company_obj = self.env["res.company"]
        t_name = "test_search_or_create"
        #
        # Test #1: Record creation
        #
        t_vals = {"name": t_name}
        partner_obj.search([("name", "=", t_name)]).unlink()
        is_new, record_ids = partner_obj.search_or_create(t_vals)
        record = partner_obj.browse(record_ids)
        # (1) record was created
        # (2) record have field's value that was requested
        self.assertTrue(is_new)
        self.assertEqual(record.name, t_name)
        #
        # Test #2: Record searching
        #
        is_new, record_ids2 = partner_obj.search_or_create(t_vals)
        record = partner_obj.browse(record_ids2)
        # (1) record have been founded (not created)
        # (2) this the same record as in the Test #1
        self.assertFalse(is_new)
        self.assertEqual(record_ids[0], record_ids2[0])
        #
        # Test #3: Record creation (x2x fields)
        #
        t_child_1 = partner_obj.create({"name": "TestChild1"})
        t_child_2 = partner_obj.create({"name": "TestChild2"})
        t_company = company_obj.create({"name": "TestCompany"})
        t_vals = {
            "name": "TestParent",
            "child_ids": [(4, t_child_1.id, 0), (4, t_child_2.id, 0)],
            "company_id": t_company.id,
        }
        is_new, record_ids3 = partner_obj.search_or_create(t_vals)
        record = partner_obj.browse(record_ids3)
        # (1) record was created
        # (2) record have x2x field's values that were requested?
        self.assertTrue(is_new)
        self.assertEqual([t_child_1.id, t_child_2.id], record.child_ids.ids)
        self.assertEqual(record.company_id.id, t_company.id)
        #
        # Test #4: Record searching (x2many fields are ignored)
        #
        is_new, record_ids4 = partner_obj.search_or_create(t_vals)
        # (1) record have been founded (not created)
        # (2) this is the same record as in the Test #3
        self.assertFalse(is_new)
        self.assertEqual(record_ids3[0], record_ids4[0])

    def test_search_read_nested(self):
        # Define test variables
        partner_obj = self.env["res.partner"]
        country_obj = self.env["res.country"]
        company_obj = self.env["res.company"]
        category_obj = self.env["res.partner.category"]
        t_country_1 = country_obj.create({"name": "TestCountry1", "code": "xxx"})
        t_country_2 = country_obj.create({"name": "TestCountry2", "code": "yyy"})
        t_company_1 = company_obj.create(
            {"name": "TestCompany1", "country_id": t_country_1.id}
        )
        t_company_2 = company_obj.create(
            {"name": "TestCompany2", "country_id": t_country_2.id}
        )
        t_category_1 = category_obj.create({"name": "TestCategory1"})
        t_category_2 = category_obj.create({"name": "TestCategory2"})
        t_category_3 = category_obj.create({"name": "TestCategory3"})
        t_category_4 = category_obj.create({"name": "TestCategory4"})
        t_partner_1 = partner_obj.create(
            {
                "name": "TestPartner1",
                "company_id": t_company_1.id,
                "category_id": [(4, t_category_1.id, 0), (4, t_category_2.id, 0)],
                "street": "TestStreet",
            }
        )
        t_partner_2 = partner_obj.create(
            {
                "name": "TestPartner2",
                "company_id": t_company_2.id,
                "category_id": [(4, t_category_3.id, 0), (4, t_category_4.id, 0)],
                "street": "TestStreet",
            }
        )
        correct_result = [
            {
                "name": t_partner_1.name,
                "category_id": [
                    {"id": t_category_1.id, "name": t_category_1.name},
                    {"id": t_category_2.id, "name": t_category_2.name},
                ],
                "company_id": {
                    "id": t_company_1.id,
                    "name": t_company_1.name,
                    "country_id": {"id": t_country_1.id, "name": t_country_1.name},
                },
            },
            {
                "name": t_partner_2.name,
                "category_id": [
                    {"id": t_category_3.id, "name": t_category_3.name},
                    {"id": t_category_4.id, "name": t_category_4.name},
                ],
                "company_id": {
                    "id": t_company_2.id,
                    "name": t_company_2.name,
                    "country_id": {"id": t_country_2.id, "name": t_country_2.name},
                },
            },
        ]
        #
        # Test 1: Record searching-reading
        #
        search_domain = [("street", "=", "TestStreet")]
        show_fields = [
            "name",
            "category_id.id",
            "category_id.name",
            "company_id.id",
            "company_id.name",
            "company_id.country_id.name",
            "company_id.country_id.id",
        ]
        delimeter = "."
        record_list = partner_obj.search_read_nested(
            domain=search_domain, fields=show_fields, delimeter=delimeter
        )
        # (1) records has requested values
        self.assertEqual(correct_result, record_list)

    def test_create_or_update_by_external_id(self):
        partner_obj = self.env["res.partner"]
        company_obj = self.env["res.company"]
        t_company_ext_id = "ext.company_1"
        t_child_1_ext_id = "ext.child_1"
        t_child_2_ext_id = "ext.child_2"
        #
        # Test #0: Check correct creation of external id
        #
        t_company = company_obj.browse(
            company_obj.create_or_update_by_external_id(
                {"id": t_company_ext_id, "name": "TestCompany"}
            )[1]
        )
        t_child_1 = partner_obj.browse(
            partner_obj.create_or_update_by_external_id(
                {"id": t_child_1_ext_id, "name": "TestChild1"}
            )[1]
        )
        t_child_2 = partner_obj.browse(
            partner_obj.create_or_update_by_external_id(
                {"id": t_child_2_ext_id, "name": "TestChild2"}
            )[1]
        )
        # (1) Check field value (correctness of creation)
        # (2) Check field value (correctness of creation)
        # (3) Check field value (correctness of creation)
        self.assertEqual(
            t_company.get_external_id()[t_company.id].split(".", 1)[1], t_company_ext_id
        )
        self.assertEqual(
            t_child_1.get_external_id()[t_child_1.id].split(".", 1)[1], t_child_1_ext_id
        )
        self.assertEqual(
            t_child_2.get_external_id()[t_child_2.id].split(".", 1)[1], t_child_2_ext_id
        )
        #
        # Test #1: Error : "External ID not defined"
        #
        t_vals = {
            "name": "John",
            "child_ids": [(4, t_child_1_ext_id, 0), (4, t_child_2_ext_id, 0)],
            "company_id": t_company_ext_id,
        }
        with self.assertRaises(ValueError):
            partner_obj.create_or_update_by_external_id(t_vals)
        #
        # Test #2: Record creation
        #
        t_vals["id"] = "ext.partner_1"
        is_new, record_id2 = partner_obj.create_or_update_by_external_id(t_vals)
        record = partner_obj.browse(record_id2)
        # (1) record was created
        # (2) record have requested external id
        # (3) record have one2many-field's value that was requested
        # (4) record have many2one-field's value that was requested
        self.assertTrue(is_new)
        self.assertEqual(record.get_external_id()[record.id], prefix + "ext.partner_1")
        self.assertEqual(record.child_ids.ids, [t_child_1.id, t_child_2.id])
        self.assertEqual(record.company_id, t_company)
        #
        # Test #3: Record update
        #
        t_vals = {"id": "ext.partner_1", "child_ids": [(3, t_child_2_ext_id, 0)]}
        is_new, record_id3 = partner_obj.create_or_update_by_external_id(t_vals)
        record = partner_obj.browse(record_id3)
        # (1) record was updated
        # (2) this is the same record (by id) that was created in Test#1
        # (3) record have one2many field's value that was requested
        self.assertFalse(is_new)
        self.assertEqual(record_id2, record_id3)
        self.assertEqual(record.child_ids.ids, [t_child_1.id])
