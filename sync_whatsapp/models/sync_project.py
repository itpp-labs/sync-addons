# Copyright 2021 Eugene Molotov <https://github.com/em230418>
# Copyright 2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import json
import logging

from requests import request

from odoo import _, api, models

from odoo.addons.multi_livechat.tools import get_multi_livechat_eval_context
from odoo.addons.sync.models.sync_project import AttrDict
from odoo.addons.sync.tools import LogExternalQuery

_logger = logging.getLogger(__name__)


class SyncProjectWhatsApp(models.Model):

    _inherit = "sync.project.context"

    @api.model
    def _eval_context_whatsapp_chatapi(self, secrets, eval_context):
        """Adds whatsapp object:"""
        params = eval_context["params"]

        if not params.WHATSAPP_CHATAPI_API_URL:
            raise Exception(_("WhatsApp Chat API URL is not set"))

        if not secrets.WHATSAPP_CHATAPI_TOKEN:
            raise Exception(_("WhatsApp Chat API token is not set"))

        def whatsapp_service_request(method, url, data=None):
            r = request(
                method,
                params.WHATSAPP_CHATAPI_API_URL.rstrip("/")
                + url
                + "?token="
                + secrets.WHATSAPP_CHATAPI_TOKEN,
                json=data,
                timeout=5,
            )
            r.raise_for_status()
            return r

        @LogExternalQuery("WhatsApp->set_webhook", eval_context)
        def set_webhook(url):
            return whatsapp_service_request(
                "post", "/webhook", {"set": True, "webhookUrl": url}
            )

        @LogExternalQuery("WhatsApp->send_message", eval_context)
        def send_message(chat_id, body):
            return whatsapp_service_request(
                "post",
                "/sendMessage",
                {
                    "chatId": chat_id,
                    "body": body,
                },
            )

        @LogExternalQuery("WhatsApp->send_file", eval_context)
        def send_file(chat_id, attachment, caption=None):
            return whatsapp_service_request(
                "post",
                "/sendFile",
                {
                    "chatId": chat_id,
                    "body": "".join(
                        [
                            "data:",
                            attachment.mimetype or "application/octet-stream",
                            ";base64,",
                            attachment.datas.decode(),
                        ]
                    ),
                    "filename": attachment.name or "unknown.bin",
                    "caption": caption or "",
                },
            )

        multi_livechat_context = AttrDict(
            get_multi_livechat_eval_context(
                self.env, "multi_livechat_whatsapp_chatapi", eval_context
            )
        )

        def whatsapp_webhook_parse(request):
            # if you are using python 3.5, json.loads with bytes argument will fail
            # note this, if you are backporting to 12.0
            request_json = json.loads(request.data)
            return request_json["messages"]

        whatsapp_service_api = AttrDict(
            {
                "set_webhook": set_webhook,
                "send_message": send_message,
                "send_file": send_file,
            }
        )

        return {
            "whatsapp_service_api": whatsapp_service_api,
            "whatsapp_webhook_parse": whatsapp_webhook_parse,
            "multi_livechat": multi_livechat_context,
        }
