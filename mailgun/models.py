import requests
import time
import dateutil
import pytz

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
