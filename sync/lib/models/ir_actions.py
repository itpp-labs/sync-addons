# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import uuid

from werkzeug import urls

from odoo import api, fields, models
from odoo.http import request
from odoo.tools.json import scriptsafe as json_scriptsafe


class ServerAction(models.Model):
    """ Add website option in server actions. """

    _inherit = "sync.trigger.webhook"

    website_path = fields.Char("Website Path")
    website_url = fields.Char(
        "Website Url",
        compute="_compute_website_url",
        help="The full URL to access the server action through the website.",
    )
    webhook_type = fields.Selection(
        [("http", "application/x-www-form-urlencoded"), ("json", "application/json")],
        string="Webhook Type",
        default="json",
    )

    def _get_website_url(self, website_path, webhook_type):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        link = (
            website_path
            or (self.action_server_id.id and "%d" % self.action_server_id.id)
            or ""
        )
        if base_url and link:
            path = "website/action-{webhook_type}/{link}".format(
                webhook_type=webhook_type, link=link
            )
            return urls.url_join(base_url, path)
        return ""

    @api.depends(
        "webhook_type",
        "action_server_id.state",
        "website_path",
    )
    def _compute_website_url(self):
        for trigger in self:
            action = trigger.action_server_id
            if action.state == "code":
                trigger.website_url = trigger._get_website_url(
                    trigger.website_path, trigger.webhook_type
                )
            else:
                trigger.website_url = False

            if not trigger.website_url:
                continue

    @api.model
    def _get_eval_context(self, action):
        """ Override to add the request object in eval_context. """
        eval_context = self.action_server_id._get_eval_context(action)
        if action.state == "code":
            eval_context["request"] = request
            eval_context["json"] = json_scriptsafe
        return eval_context

    @api.model
    def _run_action_code_multi(self, eval_context=None):
        """Override to allow returning response the same way action is already
        returned by the basic server action behavior. Note that response has
        priority over action, avoid using both.
        """
        res = self.action_server_id._run_action_code_multi(eval_context)
        return eval_context.get("response", res)

    def action_website_path(self):
        for r in self:
            r.website_path = uuid.uuid4()
