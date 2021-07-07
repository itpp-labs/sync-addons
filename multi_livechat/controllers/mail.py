# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import http
from odoo.http import request

from odoo.addons.mail.controllers.main import MailController


class MultiLivechatMailController(MailController):
    @http.route()
    def mail_init_messaging(self):
        values = super().mail_init_messaging()
        values["multi_livechat"] = request.env["mail.channel"].multi_livechat_info()
        return values
