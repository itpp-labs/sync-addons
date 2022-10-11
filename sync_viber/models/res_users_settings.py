# Copyright 2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    is_discuss_sidebar_category_viber_open = fields.Boolean(
        "Is category Viber open", default=True
    )
