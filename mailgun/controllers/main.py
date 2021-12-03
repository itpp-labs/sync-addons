import re

from odoo import http
from odoo.http import request


class MailMailgun(http.Controller):
    @http.route("/mailgun/notify", auth="public", type="http", csrf=False)
    def mailgun_notify(self, **kw):
        # mailgun notification in json format
        message_url = kw.get("message-url")
        if not re.match("^https://[^/]*api.mailgun.net/", message_url):
            # simple security check failed
            raise Exception("wrong message-url")
        request.env["mail.thread"].sudo().mailgun_fetch_message(message_url)
        return "ok"
