# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

import dateutil.parser

from odoo import _, api, exceptions, fields, models

from .. import pagadito

_logger = logging.getLogger(__name__)


class TransactionPagadito(models.Model):
    _inherit = "payment.transaction"

    @api.model
    def _pagadito_form_get_tx_from_data(self, data):
        tx_ref = data.get("ern_value")
        txs = self.search([("reference", "=", tx_ref)])
        return txs[0]

    @api.multi
    def _pagadito_form_validate(self, data):
        token_trans = data.get("value")
        # connect
        token = self.acquirer_id._pagadito_connect()
        # get_status
        status_data = self.acquirer_id._pagadito_call(
            pagadito.OP_GET_STATUS, {"token": token, "token_trans": token_trans}
        )
        if status_data.get("code") != pagadito.PG_GET_STATUS_SUCCESS:
            raise exceptions.UserError(
                _("Method get_status doesn't work:\n%s"), status_data.get("message")
            )

        status = status_data["value"].get("status")
        date_trans = status_data["value"].get("date_trans")
        if date_trans:
            date_trans = dateutil.parser.parse(date_trans)
            # TODO: shall we fix timezone?
        vals = {
            "acquirer_reference": status_data["value"].get("reference"),
        }
        if status in [pagadito.STATUS_COMPLETED]:
            _logger.info(
                "Validated Pagadito payment for tx %s: set as done" % (self.reference)
            )
            date_validate = date_trans or fields.Datetime.now()
            vals.update(state="done", date_validate=date_validate)
            return self.write(vals)

        elif status in [
            pagadito.STATUS_VERIFYING,
            pagadito.STATUS_REGISTERED,
            pagadito.STATUS_REVOKED,
            pagadito.STATUS_FAILED,
            pagadito.STATUS_CANCELED,
            pagadito.STATUS_EXPIRED,
        ]:
            _logger.info(
                "Received notification for Pagadito payment %s: set as pending"
                % (self.reference)
            )
            vals.update(state="pending", state_message=status)
            return self.write(vals)
        else:
            error = (
                "Received unrecognized status for Pagadito payment %s: %s, set as error"
                % (self.reference, status)
            )
            _logger.info(error)
            vals.update(state="error", state_message=error)
            return self.write(vals)
