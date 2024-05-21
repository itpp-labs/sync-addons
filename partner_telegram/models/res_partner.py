# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    telegram_ID = fields.Char()
    telegram = fields.Char(
        string="Telegram", compute="_compute_telegram", inverse="_inverse_telegram"
    )
    telegram_username = fields.Char()
    telegram_mobile = fields.Char()
    telegram_url = fields.Char(compute="_compute_telegram")

    @api.depends("telegram_username", "telegram_mobile")
    def _compute_telegram(self):
        for record in self:
            if record.telegram_username:
                record.telegram_url = f"https://t.me/{record.telegram_username}"
                record.telegram = record.telegram_username
            elif record.telegram_mobile:
                record.telegram_url = f"https://t.me/{record.telegram_mobile}"
                record.telegram = record.telegram_mobile
            else:
                record.telegram_url = ""

    def _inverse_telegram(self):
        for record in self:
            value = record.telegram
            if not value:
                record.telegram_username = False
                record.telegram_mobile = False
            elif value.startswith("@"):
                record.telegram_username = value[1:]
            elif value.startswith("https://t.me/"):
                record.telegram_username = value[len("https://t.me/") :]
            elif value.startswith("+"):
                record.telegram_mobile = value.replace("-", "").replace(" ", "")
