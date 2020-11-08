# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import json

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SyncProject1c(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(selection_add=[("1c", "1c")])

    @api.model
    def _eval_context_1c(self, secrets, eval_context):
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all([params.ODATA_URL, secrets.ODATA_USERNAME, secrets.ODATA_PASSWORD]):
            raise UserError(_("1c Credentials are not set"))

        def odata_request(method, name, url_data=None, body_data=None):
            if not url_data:
                url_data = {}
            url_data.setdefault("$format", "json")
            if body_data:
                body_data = json.dumps(body_data)
            url = params.ODATA_URL + name
            auth = (secrets.ODATA_USERNAME, secrets.ODATA_PASSWORD)
            log_transmission(
                "1C Server", "{} {}\n{}\n\n{}".format(method, url, url_data, body_data)
            )
            r = requests.request(
                method, url, params=url_data, data=body_data, auth=auth
            )
            log("RESPONSE: {}\n{}".format(r.status_code, r.text))
            return r.json()

        return {"odata_request": odata_request}
