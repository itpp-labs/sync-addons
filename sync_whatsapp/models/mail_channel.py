# Copyright 2021 Eugene Molotov <https://github.com/em230418>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    channel_type = fields.Selection(
        selection_add=[("multi_livechat_whatsapp_chatapi", "WhatsApp (Chat API)")],
        ondelete={"multi_livechat_whatsapp_chatapi": "cascade"},
    )
