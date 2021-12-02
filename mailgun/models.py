# -*- coding: utf-8 -*-
import logging

import requests
from openerp import api, models

try:
    import simplejson as json
except ImportError:
    import json

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def mailgun_fetch_message(self, message_url):
        api_key = self.env["ir.config_parameter"].sudo().get_param("mailgun.apikey")
        res = requests.get(
            message_url,
            headers={"Accept": "message/rfc2822"},
            auth=("api", api_key),
            verify=False,
        )
        self.message_process(False, res.json().get("body-mime"))


class IrConfigParameter(models.Model):
    _inherit = ["ir.config_parameter"]

    @api.model
    def mailgun_verify(self):
        verified = self.get_param("mailgun.verified")
        if verified:
            return
        api_key = self.get_param("mailgun.apikey")
        mail_domain = self.get_param("mail.catchall.domain")
        if api_key and mail_domain:
            url = "https://api.mailgun.net/v3/domains/%s/verify" % mail_domain
            res = requests.put(url, auth=("api", api_key))
            if (
                res.status_code == 200
                and json.loads(res.text)["domain"]["state"] == "active"
            ):
                self.set_param("mailgun.verified", "1")
