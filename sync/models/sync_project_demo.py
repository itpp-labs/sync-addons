# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import json
import xmlrpc.client as _client
from math import sqrt

# https://github.com/python-telegram-bot/python-telegram-bot
from telegram import Bot, Update

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.queue_job.exception import RetryableJobError

from .ir_logging import LOG_WARNING
from .sync_project import AttrDict


class SyncProjectDemo(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(
        selection_add=[
            ("odoo2odoo", "Odoo2odoo"),
            ("telegram", "Telegram"),
            ("trello_github", "Trello & Github"),
        ]
    )

    @api.model
    def _eval_context_odoo2odoo(self, secrets, eval_context):
        """
        Additional functions to access external Odoo:

        * odoo_execute_kw(model, method, *args, **kwargs)

          Connection is established according to following parameters:

          params.URL
          params.DB
          secrets.USERNAME
          secrets.PASSWORD
        """
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all([params.URL, params.DB, secrets.USERNAME, secrets.PASSWORD]):
            raise UserError(_("External Odoo Credentials are not set"))

        def odoo_execute_kw(model, method, *args, **kwargs):
            log_transmission(
                "XMLRPC DB={} URL={}".format(params.DB, params.URL),
                json.dumps([method, args, kwargs]),
            )
            try:
                common = _client.ServerProxy("{}/xmlrpc/2/common".format(params.URL))
                uid = common.authenticate(
                    params.DB, secrets.USERNAME, secrets.PASSWORD, {}
                )
                models = _client.ServerProxy("{}/xmlrpc/2/object".format(params.URL))
            except OSError:
                raise RetryableJobError("Error on connecting to external Odoo")
            res = models.execute_kw(
                params.DB, uid, secrets.PASSWORD, model, method, args, kwargs
            )
            log("Response: %s" % res, level="debug")
            return res

        return {
            "odoo_execute_kw": odoo_execute_kw,
        }

    @api.model
    def _eval_context_telegram(self, secrets, eval_context):
        """Adds telegram object:

        * telegram.sendMessage
        * telegram.setWebhook
        * telegram.parse_data
        """
        from odoo.tools import html2plaintext
        from lxml.html.clean import Cleaner

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

    @api.model
    def _eval_context_trello_github(self, secrets, eval_context):
        """Adds trello and github object with set of available methods (see sync/models/sync_project_demo.py):
        * trello
        * github

        It also adds two consts:

        * GITHUB="github"
        * TRELLO="trello"

        And math function:

        * sqrt

        """
        GITHUB = "github"
        TRELLO = "trello"
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]

        # closure is not really needed, but let's keep as it was done in previous
        # version when it was mandatory
        def _trello(secrets):
            for key in ["TRELLO_TOKEN", "TRELLO_KEY", "TRELLO_BOARD_ID"]:
                if not getattr(secrets, key):
                    raise Exception("{} is not set".format(key))

            # https://github.com/sarumont/py-trello/tree/master/trello
            from trello import TrelloClient
            from trello.exceptions import ResourceUnavailable

            client = TrelloClient(
                api_key=secrets.TRELLO_KEY, api_secret=secrets.TRELLO_TOKEN,
            )
            board = client.get_board(secrets.TRELLO_BOARD_ID)

            # Webhook
            def set_webhook(url):
                id_model = board.id
                desc = "Demo Trello-Github Integration"
                log_transmission(
                    TRELLO, "set webhook: {}".format([url, id_model, desc])
                )

                # original create_hook is not used. See: https://github.com/sarumont/py-trello/pull/323
                # hook = client.create_hook(url, id_model, desc, token=secrets.TRELLO_TOKEN)
                token = secrets.TRELLO_TOKEN
                res = client.fetch_json(
                    "tokens/{}/webhooks/".format(token),
                    http_method="POST",
                    post_args={
                        "callbackURL": url,
                        "idModel": id_model,
                        "description": desc,
                    },
                )
                log("Trello response: %s" % json.dumps(res))

            def delete_webhooks():
                for hook in client.list_hooks(secrets.TRELLO_TOKEN):
                    if hook.id_model == board.id:
                        log_transmission(
                            TRELLO, "delete webhook: {}".format([hook.callback_url])
                        )
                        hook.delete()

            # Trello cards
            def card_create(name, issue_id):
                description = "https://github.com/{}/issues/{}".format(
                    secrets.GITHUB_REPO, issue_id
                )
                log_transmission(TRELLO, "create: {}".format([name, description]))
                card_list = board.open_lists()[0]
                card = card_list.add_card(name, description)
                return card.id

            def card_add_labels(card_id, tlabel_ids):
                log_transmission(
                    TRELLO, "add labels to card#{}: {}".format(card_id, tlabel_ids)
                )
                card = client.get_card(card_id)
                for label_id in tlabel_ids:
                    try:
                        label = client.get_label(label_id, board.id)
                    except ResourceUnavailable:
                        log("Label is deleted in trello: %s" % label_id, LOG_WARNING)
                        continue
                    if label_id in card.idLabels:
                        log("Label is already in card: %s" % label)
                        continue
                    card.add_label(label)

            def card_remove_labels(card_id, tlabel_ids):
                log_transmission(
                    TRELLO, "remove labels from card#{}: {}".format(card_id, tlabel_ids)
                )
                card = client.get_card(card_id)
                for label_id in tlabel_ids:
                    label = client.get_label(label_id, board.id)
                    if label_id not in card.idLabels:
                        log("Label is already removed: %s" % label)
                        continue
                    card.remove_label(label)

            def card_add_message(card_id, message):
                log_transmission(
                    TRELLO, "add message to card#{}: {}".format(card_id, message)
                )
                card = client.get_card(card_id)
                card.comment(message)

            # Trello labels
            def label_create(name, color):
                log_transmission(TRELLO, "create label: %s" % (name))
                label = board.add_label(name, color)
                return label.id

            def label_delete(tlabel_id):
                log_transmission(TRELLO, "delete label: %s" % (tlabel_id))
                board.delete_label(tlabel_id)

            def label_update(tlabel_id, new_name, new_color):
                log_transmission(
                    TRELLO,
                    "label#{} update: {}".format(tlabel_id, [new_name, new_color]),
                )
                res = client.fetch_json(
                    "/labels/{}".format(tlabel_id),
                    http_method="PUT",
                    post_args={"id": tlabel_id, "name": new_name, "color": new_color},
                )
                log("Trello response: {}".format(res))

            def get_labels_colors():
                return {lb.id: lb.color for lb in board.get_labels()}

            def get_all_cards():
                return [
                    {"id": card.id, "idLabels": card.idLabels}
                    for card in board.all_cards()
                ]

            return AttrDict(
                {
                    "set_webhook": set_webhook,
                    "delete_webhooks": delete_webhooks,
                    "card_create": card_create,
                    "card_add_labels": card_add_labels,
                    "card_remove_labels": card_remove_labels,
                    "card_add_message": card_add_message,
                    "label_create": label_create,
                    "label_delete": label_delete,
                    "label_update": label_update,
                    "get_labels_colors": get_labels_colors,
                    "get_all_cards": get_all_cards,
                }
            )

        # Github
        def _github(secrets):
            # https://pygithub.readthedocs.io/en/latest/
            from github import Github
            from github.GithubException import UnknownObjectException

            if not secrets.GITHUB_TOKEN:
                raise Exception("github token is not set")
            if not secrets.GITHUB_REPO:
                raise Exception("github repo is not set")

            g = Github(secrets.GITHUB_TOKEN)
            repo = g.get_repo(secrets.GITHUB_REPO)

            # Github Webhook
            def set_webhook(url, events):
                # API: https://docs.github.com/en/rest/reference/repos#create-a-repository-webhook
                # Events: https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads
                config = {"url": url, "content_type": "json"}
                log_transmission(GITHUB, "set webhook: {}".format([config, events]))
                repo.create_hook("web", config, events)

            # Github Issues
            def issue_add_labels(issue_id, glabel_ids):
                issue = repo.get_issue(int(issue_id))
                labels = ids2labels(glabel_ids)
                log_transmission(GITHUB, "add labels: {}".format([issue_id, labels]))
                for lb in labels:
                    issue.add_to_labels(lb)

            def issue_remove_labels(issue_id, glabel_ids):
                issue = repo.get_issue(int(issue_id))
                labels = ids2labels(glabel_ids)
                log_transmission(GITHUB, "remove labels: {}".format([issue_id, labels]))
                for lb in labels:
                    issue.remove_from_labels(lb)

            # Github Labels
            def ids2labels(glabel_ids):
                # the arg is list of str!
                res = []
                for label in repo.get_labels():
                    if str(label.raw_data["id"]) in glabel_ids:
                        res.append(label)
                return res

            def label_create(name, color):
                # check first if label already exist:
                label = None
                try:
                    log_transmission(GITHUB, "get label: %s" % (name))
                    label = repo.get_label(name)
                except UnknownObjectException:
                    pass
                if not label:
                    log_transmission(GITHUB, "create label: %s" % (name))
                    label = repo.create_label(name, color)
                return label.raw_data["id"]

            def label_delete(glabel_id):
                labels = ids2labels([int(glabel_id)])
                lb = labels[0]
                log_transmission(GITHUB, "delete label: {}".format([lb]))
                lb.delete()

            def label_update(glabel_id, new_name, new_color):
                labels = ids2labels([int(glabel_id)])
                lb = labels[0]
                log_transmission(
                    GITHUB, "update label: {}".format([lb, new_name, new_color])
                )
                lb.edit(new_name, new_color)

            def get_all_issues(page=None):
                issues = repo.get_issues()
                if page is not None:
                    issues = issues.get_page(page)
                return [
                    {
                        "id": issue.number,
                        "name": issue.title,
                        "labels": issue.raw_data["labels"],
                        "body": issue.body,
                    }
                    for issue in issues
                ]

            return AttrDict(
                {
                    "set_webhook": set_webhook,
                    "issue_add_labels": issue_add_labels,
                    "issue_remove_labels": issue_remove_labels,
                    "label_create": label_create,
                    "label_delete": label_delete,
                    "label_update": label_update,
                    "get_all_issues": get_all_issues,
                }
            )

        return {
            "github": _github(secrets),
            "trello": _trello(secrets),
            "GITHUB": GITHUB,
            "TRELLO": TRELLO,
            "sqrt": sqrt,
        }
