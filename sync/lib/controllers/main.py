# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import werkzeug

from odoo import http
from odoo.http import request


class Website(http.Controller):
    def actions_server(self, path_or_xml_id_or_id, **post):
        trigger = request.env["sync.trigger.webhook"]
        action = None

        action = trigger.sudo().search(
            [
                ("website_path", "=", path_or_xml_id_or_id),
                ("website_published", "=", True),
            ],
            limit=1,
        )
        # run it, return only if we got a Response object
        if action:
            if action.state == "code" and action.website_published:
                action_res = action.action_server_id.run()
                if isinstance(action_res, werkzeug.wrappers.Response):
                    return action_res

        return request.redirect("/")
