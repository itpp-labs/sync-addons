import requests
import time
import dateutil
import pytz
import simplejson

from openerp import models, api

from openerp.addons.mail.models.mail_message import decode
from openerp.addons.mail.models.mail_thread import mail_header_msgid_re

import logging
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def mailgun_fetch_message(self, message_url):
        api_key = self.env['ir.config_parameter'].sudo().get_param('mailgun.apikey')
        res = requests.get(message_url, headers={'Accept': 'message/rfc2822'}, auth=('api', api_key))
        self.message_process(False, res.json().get('body-mime'))


class IrConfigParameter(models.Model):
    _inherit = ['ir.config_parameter']

    @api.model
    def mailgun_verify(self):
        api_key = self.get_param('mailgun.apikey')
        mail_domain = self.get_param('mail.catchall.domain')
        cron_record = self.env.ref('base.mailgun_domain_verification')
        if api_key and mail_domain:
            url = "https://api.mailgun.net/v3/domains/%s/verify" % mail_domain
            res = requests.put(url, auth=("api", api_key))
            if res.status_code == 200 and simplejson.loads(res.text)["domain"]["sate"] == "active":
                cron_record.write({'active': False})
