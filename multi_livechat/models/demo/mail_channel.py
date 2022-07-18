# Copyright 2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    channel_type = fields.Selection(
        selection_add=[("multi_livechat_echo_demo", "ECHO (Demo)")],
        ondelete={"multi_livechat_echo_demo": "cascade"},
    )
