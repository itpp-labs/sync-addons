# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http

from ..lib.controllers.main import Website


class Webhook(Website):
    @http.route(
        [
            "/website/action-json/<path_or_xml_id_or_id>",
            "/website/action-json/<path_or_xml_id_or_id>/<path:path>",
        ],
        type="json",
        auth="public",
        website=True,
        csrf=False,
    )
    def actions_server_json(self, path_or_xml_id_or_id, **post):
        res = self.actions_server(path_or_xml_id_or_id, **post)
        return res.data

    @http.route(
        [
            "/website/action-http/<path_or_xml_id_or_id>",
            "/website/action-http/<path_or_xml_id_or_id>/<path:path>",
        ],
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def actions_server_http(self, path_or_xml_id_or_id, **post):
        return self.actions_server(path_or_xml_id_or_id, **post)
