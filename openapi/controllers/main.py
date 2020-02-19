# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import json
import logging

import werkzeug

from odoo import http

from odoo.addons.web.controllers.main import ensure_db
from odoo.addons.web_settings_dashboard.controllers.main import WebSettingsDashboard

_logger = logging.getLogger(__name__)


class OpenapiWebSettingsDashboard(WebSettingsDashboard):
    @http.route("/web_settings_dashboard/data", type="json", auth="user")
    def web_settings_dashboard_data(self, **kw):

        result = super(OpenapiWebSettingsDashboard, self).web_settings_dashboard_data(
            **kw
        )

        namespaces = http.request.env["openapi.namespace"].search([])

        # TODO: replace dummy data
        namespace_list = [
            {
                "id": n.id,
                "name": n.name,
                "models_count": n.access_ids.search_count([]),
                "create_count": 10,
                "read_count": 123,
                "update_count": 55,
                "delete_count": 0,
                "last_connection": n.last_log_date,
            }
            for n in namespaces
        ]

        result.update({"openapi": {"namespace_list": namespace_list,}})

        return result


class OAS(http.Controller):
    @http.route(
        "/api/v1/<namespace_name>/swagger.json",
        type="http",
        auth="none",
        csrf=False,
        cors="*",
    )
    def OAS_json_spec_download(self, namespace_name, **kwargs):
        ensure_db()
        namespace = (
            http.request.env["openapi.namespace"]
            .sudo()
            .search([("name", "=", namespace_name)])
        )
        if not namespace:
            raise werkzeug.exceptions.NotFound()
        if namespace.token != kwargs.get("token"):
            raise werkzeug.exceptions.Forbidden()

        response_params = {"headers": [("Content-Type", "application/json")]}
        if "download" in kwargs:
            response_params = {
                "headers": [
                    ("Content-Type", "application/octet-stream; charset=binary"),
                    ("Content-Disposition", http.content_disposition("swagger.json")),
                ],
                "direct_passthrough": True,
            }

        return werkzeug.wrappers.Response(
            json.dumps(namespace.get_OAS()), status=200, **response_params
        )
