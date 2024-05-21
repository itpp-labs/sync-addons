# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase


class TestResPartnerTelegram(TransactionCase):
    def setUp(self):
        super(TestResPartnerTelegram, self).setUp()
        self.ResPartner = self.env["res.partner"]
        # Create a partner without telegram information
        self.partner = self.ResPartner.create({"name": "Test"})

    def test_telegram_set_username(self):
        # Set the telegram field with a username
        self.partner.telegram = "@testuser"

        # Check the computed fields
        self.assertEqual(self.partner.telegram_username, "testuser")
        self.assertEqual(self.partner.telegram_url, "https://t.me/testuser")
        self.assertEqual(self.partner.telegram, "testuser")

    def test_telegram_set_mobile(self):
        # Set the telegram field with a mobile number
        self.partner.telegram = "+1234567890"

        # Check the computed fields
        self.assertEqual(self.partner.telegram_mobile, "+1234567890")
        self.assertEqual(self.partner.telegram_url, "https://t.me/+1234567890")
        self.assertEqual(self.partner.telegram, "+1234567890")

    def test_telegram_set_url(self):
        # Set the telegram field with a URL
        self.partner.telegram = "https://t.me/testuser"

        # Check the computed fields
        self.assertEqual(self.partner.telegram_username, "testuser")
        self.assertEqual(self.partner.telegram_url, "https://t.me/testuser")
        self.assertEqual(self.partner.telegram, "testuser")

    def test_telegram_clear(self):
        # Set the telegram field and then clear it
        self.partner.telegram = "@testuser"
        self.partner.telegram = ""

        # Check the computed fields
        self.assertFalse(self.partner.telegram_username)
        self.assertFalse(self.partner.telegram_mobile)
        self.assertFalse(self.partner.telegram_url)
        self.assertFalse(self.partner.telegram)
