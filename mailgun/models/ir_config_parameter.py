import logging

import requests

from odoo import api, models

try:
    import simplejson as json
except ImportError:
    import json


_logger = logging.getLogger(__name__)


class IrConfigParameter(models.Model):
    _inherit = ["ir.config_parameter"]

    @api.model
    def mailgun_verify(self):
        verified = self.sudo().get_param("mailgun.verified")
        if verified:
            return
        api_key = self.sudo().get_param("mailgun.apikey")
        mail_domain = self.sudo().get_param("mail.catchall.domain")
        if api_key and mail_domain:
            url = "https://api.mailgun.net/v3/domains/%s/verify" % mail_domain
            res = requests.put(url, auth=("api", api_key))
            if (
                res.status_code == 200
                and json.loads(res.text)["domain"]["state"] == "active"
            ):
                self.sudo().set_param("mailgun.verified", "1")
