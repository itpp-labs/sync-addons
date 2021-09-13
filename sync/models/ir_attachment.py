# Copyright 2021 ilya ilchenko <http://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import models


class Attachment(models.Model):
    _inherit = "ir.attachment"

    def get_public_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        self.generate_access_token()
        return "%s/web/content/%s/%s?access_token=%s" % (
            base_url,
            self.id,
            self.name,
            self.access_token,
        )
