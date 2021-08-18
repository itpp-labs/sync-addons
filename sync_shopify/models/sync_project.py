# Copyright 2021 Eugene Molotov <https://github.com/em230418>
# License MIT (https://opensource.org/licenses/MIT).
from requests import request
from requests.auth import HTTPBasicAuth

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SyncProjectShopify(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(selection_add=[("shopify", "Shopify")])

    @api.model
    def _eval_context_shopify(self, secrets, eval_context):
        """Adds tools for Shopify API:
        shopify_api_request: Wrapper to make HTTP requests to shopify admin api
        """
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all(
            [
                params.SHOP_DOMAIN,
                params.API_VERSION,
                secrets.API_KEY,
                secrets.API_SECRET,
            ]
        ):
            raise UserError(_("Shopify Admin API Credentials are not set"))

        def shopify_api_request(method, endpoint, data=None, **kwargs):
            log_transmission(
                "Shopify",
                "{} {}\n{}\n{}".format(method.upper(), endpoint, data, kwargs),
            )
            method = method.lower()
            url = (
                "https://"
                + params.SHOP_DOMAIN
                + "/admin/api/"
                + params.API_VERSION
                + "/"
                + endpoint
                + ".json"
            )
            r = request(
                method,
                url,
                timeout=10,
                auth=HTTPBasicAuth(secrets.API_KEY, secrets.API_SECRET),
                json=data,
            )
            log("RESPONSE: {}\n{}".format(r.status_code, r.text))
            r.raise_for_status()
            return r.json()

        return {
            "shopify_api_request": shopify_api_request,
        }
