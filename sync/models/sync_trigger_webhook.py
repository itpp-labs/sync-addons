# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import uuid

from odoo import api, fields, models
from odoo.http import Response, request

from .ir_logging import LOG_DEBUG


class SyncTriggerWebhook(models.Model):

    _name = "sync.trigger.webhook"
    _inherit = [
        "sync.trigger.mixin",
        "sync.trigger.mixin.model_id",
        "sync.trigger.mixin.actions",
    ]
    _description = "Webhook Trigger"
    _sync_handler = "handle_webhook"
    _default_name = "Webhook"

    action_server_id = fields.Many2one(
        "ir.actions.server", delegate=True, required=True, ondelete="cascade"
    )
    active = fields.Boolean(default=True)
    webhook_type = fields.Selection(
        [("http", "application/x-www-form-urlencoded"), ("json", "application/json")],
        string="Webhook Type",
        default="json",
    )
    website_url = fields.Char("Webhook URL", compute="_compute_website_url")

    @api.depends(
        "webhook_type",
        "action_server_id.state",
        "action_server_id.website_published",
        "action_server_id.website_path",
        "action_server_id.xml_id",
    )
    def _compute_website_url(self):
        for r in self:
            website_url = r.action_server_id.website_url
            if not website_url:
                continue
            website_url = website_url.replace(
                "/website/action/", "/website/action-%s/" % r.webhook_type
            )
            r.website_url = website_url

    @api.model
    def default_get(self, fields):
        vals = super(SyncTriggerWebhook, self).default_get(fields)
        vals["website_published"] = True
        vals["groups_id"] = [(4, self.env.ref("base.group_public").id, 0)]
        vals["website_path"] = uuid.uuid4()
        return vals

    def action_website_path(self):
        for r in self:
            r.website_path = uuid.uuid4()

    def start(self):
        record = self.sudo()
        if record.active:
            start_result = record.sync_task_id.start(
                record, args=(request.httprequest,)
            )
            if not start_result:
                return self.make_response("Task or Project is disabled", 404)

            _job, (result, log) = start_result
            return self._process_handler_result(result, log)
        else:
            return self.make_response("This webhook is disabled", 404)

    def get_code(self):
        return (
            """
action = env["sync.trigger.webhook"].browse(%s).start()
"""
            % self.id
        )

    @api.model
    def _process_handler_result(self, result, log):
        if not result:
            result = "OK"
        data = None
        headers = []
        status = 200
        if isinstance(result, tuple):
            if len(result) == 3:
                data, status, headers = result
            elif len(result) == 2:
                data, status = result
        else:
            data = result
        log("Webhook response: {} {}\n{}".format(status, headers, data), LOG_DEBUG)
        return self.make_response(data, status, headers)

    @api.model
    def make_response(self, data, status=200, headers=None):
        return Response(data, status=status, headers=headers)
