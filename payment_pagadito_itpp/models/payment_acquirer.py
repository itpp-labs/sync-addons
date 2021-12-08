# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import json
import logging

from odoo import _, api, exceptions, fields, models
from odoo.http import request

from .. import pagadito

_logger = logging.getLogger(__name__)

try:
    import urlparse
    from zeep import xsd
except ImportError as err:
    _logger.debug(err)


class AcquirerPagadito(models.Model):
    _inherit = "payment.acquirer"

    provider = fields.Selection(selection_add=[("pagadito", "Pagadito")])
    pagadito_uid = fields.Char(
        "UID",
        help="El identificador del Pagadito Comercio",
        required_if_provider="pagadito",
    )
    pagadito_wsk = fields.Char(
        "WSK", help="La clave de acceso", required_if_provider="pagadito"
    )

    @api.multi
    def _pagadito_connect(self, sandbox=True):
        res = self._pagadito_call(
            pagadito.OP_CONNECT, {"uid": self.pagadito_uid, "wsk": self.pagadito_wsk}
        )
        if res.get("code") != pagadito.PG_CONNECT_SUCCESS:
            raise exceptions.UserError(
                _("Method Connect doesn't work. Wrong credentials?\n%s"),
                res.get("message"),
            )
        return res["value"]

    @api.multi
    def _pagadito_call(self, operation, params):
        sandbox = self.environment != "prod"
        return pagadito.call(operation, params, sandbox=sandbox)

    @api.multi
    def pagadito_form_generate_values(self, values):
        reference = values["reference"]
        if reference == "/":
            # we are on /shop/payment
            # -- selecting payment method screen only
            return values
        # connect
        token = self._pagadito_connect()
        # exec_trans
        order = request.website.sale_get_order()
        details = self._order2pagadito_details(order)
        custom_params = {"param1": order.name}
        res = self._pagadito_call(
            pagadito.OP_EXEC_TRANS,
            {
                "token": token,
                "ern": reference,
                "amount": order.amount_total,
                "details": json.dumps(details),
                "currency": self._currency2pagadito_code(order.currency_id),
                "custom_params": json.dumps(custom_params),
                "allow_pending_payments": "false",  # TODO: What is that?
                "extended_expiration": xsd.SkipValue,
            },
        )
        if res.get("code") != pagadito.PG_EXEC_TRANS_SUCCESS:
            raise exceptions.UserError(
                _("Method Connect doesn't work:\n%s"), res.get("message")
            )
        raw_url = res["value"]
        parsed = urlparse.urlparse(raw_url)
        pagadito_url = raw_url.split("?")[0]
        pagadito_args = urlparse.parse_qs(parsed.query)
        values["pagadito_url"] = pagadito_url
        values["pagadito_args"] = pagadito_args
        return values

    @api.model
    def _currency2pagadito_code(self, currency):
        code = currency.name
        assert code in pagadito.SUPPORTED_CURRENCY
        return code

    @api.model
    def _order2pagadito_details(self, order):
        res = []
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        for line in order.order_line:
            res.append(
                {
                    "quantity": line.product_uom_qty,
                    "description": line.name.replace("\n", " | "),
                    "price": line.price_unit,
                    "url_product": "%s/shop/product/%s"
                    % (base_url, line.product_id.product_tmpl_id.id),
                }
            )
        return res
