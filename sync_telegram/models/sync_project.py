# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import json
import logging

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

        if secrets.TELEGRAM_BOT_TOKEN:
            bot = Bot(token=secrets.TELEGRAM_BOT_TOKEN)
        else:
            raise Exception("Telegram bot token is not set")

        def sendMessage(chat_id, *args, **kwargs):
            log_transmission(
                "Message to %s@telegram" % chat_id, json.dumps([args, kwargs])
            )
            bot.sendMessage(chat_id, *args, **kwargs)

        def setWebhook(*args, **kwargs):
            log_transmission("Telegram->setWebhook", json.dumps([args, kwargs]))
            bot.setWebhook(*args, **kwargs)

        def parse_data(data):
            return Update.de_json(data, bot)

        telegram = AttrDict(
            {
                "sendMessage": sendMessage,
                "setWebhook": setWebhook,
                "parse_data": parse_data,
            }
        )

        return {
            "telegram": telegram,
            "html2plaintext": html2plaintext,
            "Cleaner": Cleaner,
        }
