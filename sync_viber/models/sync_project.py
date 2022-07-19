# Copyright 2021-2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from viberbot import Api
from viberbot.api import messages as viber_messages, viber_requests
from viberbot.api.bot_configuration import BotConfiguration

from odoo import _, api, models
from odoo.tools.safe_eval import wrap_module

from odoo.addons.multi_livechat.tools import get_multi_livechat_eval_context
from odoo.addons.sync.models.sync_project import AttrDict
from odoo.addons.sync.tools import LogExternalQuery

_logger = logging.getLogger(__name__)

# Check README for details
MAX_DOC_SIZE = 52_428_800
MAX_PHOTO_SIZE = 1_048_576
MAX_VIDEO_SIZE = 27_262_976


class SyncProjectViber(models.Model):

    _inherit = "sync.project.context"

    @api.model
    def _eval_context_viber(self, secrets, eval_context):
        """Adds viber object:
        - viber_api.set_webhook
        - viber_api.send_messages
        - viber_api.get_user_details

        - viber_requests.ViberMessageRequest
        - viber_requests.*

        - viber_messages.text_message.TextMessage
        - viber_messages.VideoMessage
        - viber_messages.*

        - viber_webhook_check
        - viber_webhook_parse

        - multi_livechat.*
        """

        params = eval_context["params"]

        if not secrets.VIBER_BOT_TOKEN:
            raise Exception(_("Viber bot token is not set"))

        company_logo = "%s/logo.png?company_id=%s" % (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url"),
            self.env.company.id,
        )
        bot_configuration = BotConfiguration(
            name=params.BOT_NAME,
            avatar=params.BOT_AVATAR_URL or company_logo,
            auth_token=secrets.VIBER_BOT_TOKEN,
        )
        viber = Api(bot_configuration)

        def viber_webhook_check(request):
            return viber.verify_signature(
                request.get_data(), request.headers.get("X-Viber-Content-Signature")
            )

        def viber_webhook_parse(request):
            vrequest = viber.parse_request(request.get_data())
            user_id = None
            if isinstance(vrequest, viber_requests.ViberMessageRequest):
                user_id = vrequest.sender.id

            if not user_id:
                try:
                    user_id = vrequest.user_id
                except AttributeError:
                    pass

            if not user_id:
                try:
                    user_id = vrequest.user.id
                except AttributeError:
                    pass

            return user_id, vrequest

        @LogExternalQuery("Viber->set_webhook", eval_context)
        def set_webhook(*args, **kwargs):
            return viber.set_webhook(*args, **kwargs)

        @LogExternalQuery("Viber->unset_webhook", eval_context)
        def unset_webhook(*args, **kwargs):
            return viber.unset_webhook(*args, **kwargs)

        @LogExternalQuery("Viber->get_user_details", eval_context)
        def get_user_details(user_id):
            return viber.get_user_details(user_id)

        @LogExternalQuery("Viber->send_messages", eval_context)
        def send_messages(to, messages):
            return viber.send_messages(to, messages)

        multi_livechat_context = AttrDict(
            get_multi_livechat_eval_context(
                self.env, "multi_livechat_viber", eval_context
            )
        )
        viber_api_context = AttrDict(
            {
                "set_webhook": set_webhook,
                "unset_webhook": unset_webhook,
                "get_user_details": get_user_details,
                "send_messages": send_messages,
            }
        )

        return {
            "viber_api": viber_api_context,
            "viber_requests": wrap_module(
                viber_requests,
                [
                    "ViberConversationStartedRequest",
                    "ViberFailedRequest",
                    "ViberMessageRequest",
                    "ViberSeenRequest",
                    "ViberSubscribedRequest",
                    "ViberUnsubscribedRequest",
                    "ViberDeliveredRequest",
                ],
            ),
            "viber_messages": wrap_module(
                viber_messages,
                [
                    "TextMessage",
                    "URLMessage",
                    "ContactMessage",
                    "PictureMessage",
                    "VideoMessage",
                    "FileMessage",
                    "LocationMessage",
                    "StickerMessage",
                    "RichMediaMessage",
                    "KeyboardMessage",
                ],
            ),
            "viber_webhook_check": viber_webhook_check,
            "viber_webhook_parse": viber_webhook_parse,
            "multi_livechat": multi_livechat_context,
            "MAX_DOC_SIZE": MAX_DOC_SIZE,
            "MAX_PHOTO_SIZE": MAX_PHOTO_SIZE,
            "MAX_VIDEO_SIZE": MAX_VIDEO_SIZE,
        }
