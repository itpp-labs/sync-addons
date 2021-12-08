# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PagaditoController(http.Controller):
    _return_url = "/payment/pagadito/confirmation"

    @http.route(_return_url, type="http", auth="none", csrf=False)
    def pagadito_confirmation(self, **data):
        _logger.debug("Pagadito confirmation data: %s", data)
        request.env["payment.transaction"].sudo().form_feedback(data, "pagadito")
        payment_validate_url = "/shop/payment/validate"
        # # following code requires website=True in http.route, but in later case form_feedback doesn't work (missed user id in sql request)
        # base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        # payment_validate_url = "%s%s" % (base_url, '/shop/payment/validate')
        return werkzeug.utils.redirect(payment_validate_url)
