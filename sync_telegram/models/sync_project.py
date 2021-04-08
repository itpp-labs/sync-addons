# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import json

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.sync.models.sync_project import AttrDict


_logger = logging.getLogger(__name__)

try:
    # https://github.com/python-telegram-bot/python-telegram-bot
    from telegram import Bot, Update  # pylint: disable=missing-manifest-dependency
except (ImportError, IOError) as err:
    _logger.debug(err)


class SyncProjectTelegram(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(selection_add=[("telegram", "Telegram"),])

    @api.model
    def _eval_context_telegram(self, secrets, eval_context):
        """Adds telegram object:
        * telegram.sendMessage
        * telegram.setWebhook
        * telegram.parse_data
        """
        from lxml.html.clean import Cleaner

        from odoo.tools import html2plaintext

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
























    # @api.model
    # def _eval_context_1c(self, secrets, eval_context):
    #     """Adds tools 1c API:
    #     * odata_request(method, name, url_data=None, body_data=None)
    #     """
    #     log_transmission = eval_context["log_transmission"]
    #     log = eval_context["log"]
    #     params = eval_context["params"]
    #     if not all([params.ODATA_URL, secrets.ODATA_USERNAME, secrets.ODATA_PASSWORD]):
    #         raise UserError(_("1c Credentials are not set"))

    #     def odata_request(method, name, url_data=None, body_data=None):
    #         if not url_data:
    #             url_data = {}
    #         url_data.setdefault("$format", "json")
    #         if body_data:
    #             body_data = json.dumps(body_data)
    #         url = params.ODATA_URL + name
    #         auth = (secrets.ODATA_USERNAME, secrets.ODATA_PASSWORD)
    #         log_transmission(
    #             "1C Server", "{} {}\n{}\n\n{}".format(method, url, url_data, body_data)
    #         )
    #         r = requests.request(
    #             method, url, params=url_data, data=body_data, auth=auth
    #         )
    #         log("RESPONSE: {}\n{}".format(r.status_code, r.text))
    #         return r.json()

    #     return {"odata_request": odata_request}
