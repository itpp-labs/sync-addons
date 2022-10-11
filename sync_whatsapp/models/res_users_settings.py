# Copyright 2022 Ivan Yelizariev <https://twitter.com/yelizariev>
from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    is_discuss_sidebar_category_whatsapp_chatapi_open = fields.Boolean(
        "Is category WhatsApp open", default=True
    )
