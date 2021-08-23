# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import base64
import logging

import requests
import telebot  # pylint: disable=missing-manifest-dependency
from lxml.html.clean import Cleaner

from odoo import api, fields, models

from odoo.addons.multi_livechat.tools import get_multi_livechat_eval_context
from odoo.addons.sync.models.sync_project import AttrDict
from odoo.addons.sync.tools import LogExternalQuery, url2base64

_logger = logging.getLogger(__name__)

MAX_SIZE_IMAGE = 10485760
MAX_SIZE_DOCUMENT = 52428800
MAX_SIZE_TO_DOWNLOAD = 20971520


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

        if secrets.TELEGRAM_BOT_TOKEN:
            bot = telebot.TeleBot(token=secrets.TELEGRAM_BOT_TOKEN)
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

        def create_mail_сhannel(partners, channel_name):
            vals = self.env["mail.channel"]._prepare_multi_livechat_channel_vals(
                "multi_livechat_telegram", channel_name, partners
            )
            return self.env["mail.channel"].sudo().create(vals)
        def url2bin(url):
            if not url:
                return None
            r = requests.get(url, timeout=42)
            return r.content

        @LogExternalQuery("Telegram->send message", eval_context)
        def sendMessage(chat_id, html, *args, **kwargs):
            bot.send_message(chat_id, _html_sanitize_telegram(html), *args, **kwargs)

        @LogExternalQuery("Telegram->send photo", eval_context)
        def sendPhoto(chat_id, datas):
            bot.send_photo(chat_id, photo=base64.b64decode(datas))

        @LogExternalQuery("Telegram->send document", eval_context)
        def sendDocument(chat_id, datas, name):
            bot.send_document(chat_id, base64.b64decode(datas), visible_file_name=name)

        def getFullPath(file_path):
            return "https://api.telegram.org/file/bot{}/{}".format(
                secrets.TELEGRAM_BOT_TOKEN, file_path
            )

        @LogExternalQuery("Telegram->get document file", eval_context)
        def getDocumentFile(chat_id, file_data):
            file_name = file_data.file_name
            file_path = bot.get_file(file_data.file_id).file_path
            content = url2bin(getFullPath(file_path))
            return [file_name, content]

        @LogExternalQuery("Telegram->get media file", eval_context)
        def getMediaFile(chat_id, file_data):
            file_path = bot.get_file(file_data.file_id).file_path
            content = url2bin(getFullPath(file_path))
            return [file_path.split("/")[-1], content]

        @LogExternalQuery("Telegram->get user photo", eval_context)
        def getUserPhoto(chat_id):
            photo_list = bot.get_user_profile_photos(chat_id).photos
            if not photo_list:
                return None
            else:
                file_path = bot.get_file(photo_list[0][0].file_id).file_path
                return url2base64(getFullPath(file_path))

        @LogExternalQuery("Telegram-> Webhook is configured", eval_context)
        def setWebhook(*args, **kwargs):
            bot.set_webhook(*args, **kwargs)

        def parse_data(data):
            return telebot.types.Update.de_json(data)

        multi_livechat_context = AttrDict(
            get_multi_livechat_eval_context(
                self.env, "multi_livechat_telegram", eval_context
            )
        )

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
                "MAX_SIZE_IMAGE": MAX_SIZE_IMAGE,
                "MAX_SIZE_DOCUMENT": MAX_SIZE_DOCUMENT,
                "MAX_SIZE_TO_DOWNLOAD": MAX_SIZE_TO_DOWNLOAD,
            }
        )

        return {
            "telegram": telegram,
            "Cleaner": Cleaner,
            "multi_livechat": multi_livechat_context,
        }
