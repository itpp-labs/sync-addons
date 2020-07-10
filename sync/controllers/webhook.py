# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import http

from odoo.addons.website.controllers.main import Website


class Webhook(http.Controller):
    @http.route(
        [
            "/website/action-json/<path_or_xml_id_or_id>",
            "/website/action-json/<path_or_xml_id_or_id>/<path:path>",
        ],
        type="json",
        # type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def actions_server(self, path_or_xml_id_or_id, **post):
        res = Website().actions_server(path_or_xml_id_or_id, **post)
        return res.data
