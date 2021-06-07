# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import base64
import json
import logging

import requests

from odoo import api, fields, models

from odoo.addons.sync.models.sync_project import AttrDict

_logger = logging.getLogger(__name__)


class SyncProjectTelegram(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(
        selection_add=[
            ("telegram", "Telegram"),
        ],
        ondelete={"telegram": "cascade"},
    )

    @api.model
    def _eval_context_telegram(self, secrets, eval_context):
        """Adds telegram object:
        * telegram.sendMessage
        * telegram.setWebhook
        * telegram.parse_data
        """
        from lxml.html.clean import Cleaner

        from odoo.tools import html2plaintext

        try:
            # https://github.com/python-telegram-bot/python-telegram-bot
            from telegram import (  # pylint: disable=missing-manifest-dependency
                Bot,
                Update,
            )
        except (ImportError, IOError) as err:
            _logger.debug(err)

        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]

        MAX_SIZE_IMAGE = 10485760
        MAX_SIZE_DOCUMENT = 52428800
        MAX_SIZE_FOR_RECEIVE = 20971520

        if secrets.TELEGRAM_BOT_TOKEN:
            bot = Bot(token=secrets.TELEGRAM_BOT_TOKEN)
        else:
            raise Exception("Telegram bot token is not set")

        def _html_sanitize_telegram(html):
            allowed_tags = set({"b", "i", "u", "s", "a", "code", "pre"})
            cleaner = Cleaner(
                safe_attrs_only=True,
                safe_attrs=set(),
                allow_tags=allowed_tags,
                remove_unknown_tags=False,
            )
            html = cleaner.clean_html(html)
            # remove surrounding div
            return html[5:-6]

        def _url2base64(url):
            r = requests.get(url)
            datas = base64.b64encode(r.content)
            return datas

        def create_mail_сhannel(partners):
            return (
                self.env["mail.channel"]
                .sudo()
                .create(
                    {
                        "channel_partner_ids": [
                            (4, partner_id) for partner_id in partners
                        ],
                        "public": "private",
                        "channel_type": "telegram",
                        "email_send": False,
                        "name": ", ".join(
                            self.env["res.partner"]
                            .sudo()
                            .browse(partners)
                            .mapped("name")
                        ),
                    }
                )
            )

        def sendMessage(chat_id, html, *args, **kwargs):
            log_transmission("%s@telegram" % chat_id, "Message: %s" % html)
            bot.sendMessage(chat_id, _html_sanitize_telegram(html), *args, **kwargs)

        def sendPhoto(chat_id, datas):
            log_transmission("%s@telegram" % chat_id, "Photo sent")
            bot.sendPhoto(chat_id, photo=base64.b64decode(datas))

        def sendDocument(chat_id, name, datas):
            log_transmission("%s@telegram" % chat_id, "Document sent")
            bot.sendDocument(chat_id, filename=name, document=base64.b64decode(datas))

        def getDocumentFile(chat_id, file_data):
            file_name = file_data.file_name
            content = bot.getFile(file_data).download_as_bytearray()
            log(
                "Attachment from telegram received: %s" % file_name,
                name="%s@telegram" % chat_id,
            )
            return [file_name, content]

        def getMediaFile(chat_id, file_data):
            file_name = bot.getFile(file_data).file_path.split("/")[-1]
            content = bot.getFile(file_data).download_as_bytearray()
            log(
                "Attachment from telegram received: %s" % file_name,
                name="%s@telegram" % chat_id,
            )
            return [file_name, content]

        def getUserPhoto(chat_id):
            photo_list = bot.getUserProfilePhotos(chat_id).photos
            if not photo_list:
                return None
            else:
                photo_path = bot.getFile(photo_list[0][0]).file_path
                log(
                    "The user's photo has been added to the partner record.",
                    name="%s@telegram" % chat_id,
                )
                return _url2base64(photo_path)

        def setWebhook(*args, **kwargs):
            log_transmission("Telegram->setWebhook", json.dumps([args, kwargs]))
            bot.setWebhook(*args, **kwargs)

        def parse_data(data):
            return Update.de_json(data, bot)

        telegram = AttrDict(
            {
                "sendMessage": sendMessage,
                "sendPhoto": sendPhoto,
                "sendDocument": sendDocument,
                "getDocumentFile": getDocumentFile,
                "getMediaFile": getMediaFile,
                "getUserPhoto": getUserPhoto,
                "setWebhook": setWebhook,
                "parse_data": parse_data,
                "create_mail_сhannel": create_mail_сhannel,
                "MAX_SIZE_IMAGE": MAX_SIZE_IMAGE,
                "MAX_SIZE_DOCUMENT": MAX_SIZE_DOCUMENT,
                "MAX_SIZE_FOR_RECEIVE": MAX_SIZE_FOR_RECEIVE,
            }
        )

        return {
            "telegram": telegram,
            "html2plaintext": html2plaintext,
            "Cleaner": Cleaner,
        }
