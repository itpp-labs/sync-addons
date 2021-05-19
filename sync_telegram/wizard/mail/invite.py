# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models


class Invite(models.TransientModel):
    _inherit = "mail.wizard.invite"

    channel_ids = fields.Many2many(
        "mail.channel", domain=[("channel_type", "not in", ["chat", "livechat"])]
    )
