# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestDefaultValue(TransactionCase):
    def setUp(self):
        super(TestDefaultValue, self).setUp()

    def test_create_record(self):
        # test variable definition
        param_obj = self.env["sync.project.param"]
        value = "Test value"
        new_value = "New value"

        # Test #1: Creating a record
        test_record = param_obj.create({"key": "TEST_KEY", "initial_value": value})
        self.assertEqual(test_record.value, value)

        # Test #2: Checking the overwrite initial_value
        test_record.write({"initial_value": new_value})
        self.assertEqual(test_record.value, value)

        # Test #3: Checking the overwrite value
        test_record.write({"value": new_value})
        self.assertEqual(test_record.value, new_value)
