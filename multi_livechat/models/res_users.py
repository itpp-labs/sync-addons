# Copyright 2021-2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models


class Users(models.Model):
    _inherit = "res.users"

    def _init_messaging(self):
        values = super()._init_messaging()
        values["multi_livechat"] = self.env["mail.channel"].multi_livechat_info()
        return values
