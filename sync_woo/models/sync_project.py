# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from woocommerce import API

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SyncProjectWoo(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(selection_add=[("woo", "WooCommerce")])

    @api.model
    def _eval_context_woo(self, secrets, eval_context):
        """Adds tools for Woo API:
        * wcapi_request -- wrapper for WooCommerce API lib  http://woocommerce.github.io/woocommerce-rest-api-docs/
        """
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all(
            [params.API_URL, params.API_VERSION, secrets.API_KEY, secrets.API_SECRET]
        ):
            raise UserError(_("WooCommerce API Credentials are not set"))

        wcapi = API(
            url=params.API_URL,
            consumer_key=secrets.API_KEY,
            consumer_secret=secrets.API_SECRET,
            wp_api=True,
            version=params.API_VERSION,
            verify_ssl=params.API_VERIFY_SSL != "0",
        )

        def wcapi_request(method, endpoint, data=None, **kwargs):
            log_transmission(
                "WooCommerce",
                "{} {}\n{}\n{}".format(method.upper(), endpoint, data, kwargs),
            )
            method = method.lower()
            if method in {"post", "put"}:
                r = getattr(wcapi, method)(endpoint, data, **kwargs)
            elif method in {"get", "delete", "options"}:
                r = getattr(wcapi, method)(endpoint, **kwargs)
            else:
                raise UserError(_("Unknown method: %s"), method)

            log("RESPONSE: {}\n{}".format(r.status_code, r.text))
            return r.json()

        return {"wcapi_request": wcapi_request}
