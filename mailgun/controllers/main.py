# -*- coding: utf-8 -*-
from openerp.addons.web import http
from openerp.addons.web.http import request
import werkzeug
import email
import requests
import simplejson

class MailMailgun(http.Controller):

    @http.route('/mailgun/notify', auth='public', type='http', csrf=False)
    def mailgun_notify(self, **kw):
        # mailgun notification in json format
        message_url = kw.get('message-url')
        request.env['mail.thread'].sudo().mailgun_fetch_message(message_url)
        return 'ok'
