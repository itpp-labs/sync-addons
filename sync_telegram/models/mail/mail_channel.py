# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    channel_type = fields.Selection(
        selection_add=[("multi_livechat_telegram", "Telegram")],
    )
