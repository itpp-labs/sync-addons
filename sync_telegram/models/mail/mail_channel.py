# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import api, fields, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    channel_type = fields.Selection(
        selection_add=[("telegram", "Telegram Conversation")]
    )

    def _compute_is_chat(self):
        super(MailChannel, self)._compute_is_chat()
        for record in self:
            if record.channel_type == "telegram":
                record.is_chat = True

    @api.model
    def channel_fetch_slot(self):
        values = super(MailChannel, self).channel_fetch_slot()
        domain = [("channel_type", "=", "telegram")]
        # pinned_channels = self.env['mail.channel.partner'].search([('partner_id', '=', self.env.user.partner_id.id), ('is_pinned', '=', True)]).mapped('channel_id')
        # domain += [('id', 'in', pinned_channels.ids)]
        values["channel_telegram"] = self.search(domain).channel_info()
        return values
