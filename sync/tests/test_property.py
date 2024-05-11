# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase


class TestProperty(TransactionCase):
    def setUp(self):
        super(TestProperty, self).setUp()
        self.project = self.env["sync.project"].create({"name": "Test Project"})
        self.env = self.env(
            context=dict(self.env.context, sync_project_id=self.project.id)
        )
        self.company = self.env.ref("base.main_company")
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_basic_types(self):
        # Basic types tests included for completeness
        self.company._set_sync_property("x_test_prop_char", "char", "Hello, World!")
        self.company._set_sync_property("x_test_prop_boolean", "boolean", True)
        self.company._set_sync_property("x_test_prop_integer", "integer", 42)
        self.company._set_sync_property("x_test_prop_float", "float", 3.14159)

        # Invalidate cache before reading
        self.env.cache.invalidate()

        # Retrieval and Assertions
        prop_char = self.company._get_sync_property("x_test_prop_char", "char")
        prop_boolean = self.company._get_sync_property("x_test_prop_boolean", "boolean")
        prop_integer = self.company._get_sync_property("x_test_prop_integer", "integer")
        prop_float = self.company._get_sync_property("x_test_prop_float", "float")

        self.assertEqual(prop_char, "Hello, World!", "The char property did not match.")
        self.assertEqual(prop_boolean, True, "The boolean property did not match.")
        self.assertEqual(prop_integer, 42, "The integer property did not match.")
        self.assertAlmostEqual(
            prop_float, 3.14159, places=5, msg="The float property did not match."
        )
