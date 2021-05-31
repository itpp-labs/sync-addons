# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020-2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import base64
import datetime
import json
import logging
import time

from pytz import timezone

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, frozendict
from odoo.tools.safe_eval import safe_eval, test_python_expr
from odoo.tools.translate import _

from odoo.addons.base.models.ir_actions import dateutil
from odoo.addons.queue_job.exception import RetryableJobError

from .ir_logging import LOG_CRITICAL, LOG_DEBUG, LOG_ERROR, LOG_INFO, LOG_WARNING

_logger = logging.getLogger(__name__)
DEFAULT_LOG_NAME = "Log"
EVAL_CONTEXT_PREFIX = "_eval_context_"


def cleanup_eval_context(eval_context):
    delete = [k for k in eval_context if k.startswith("_")]
    for k in delete:
        del eval_context[k]
    return eval_context


class SyncProject(models.Model):

    _name = "sync.project"
    _description = "Sync Project"

    name = fields.Char(
        "Name", help="e.g. Legacy Migration or eCommerce Synchronization", required=True
    )
    active = fields.Boolean(default=True)
    eval_context = fields.Selection([], string="Evaluation context")
    eval_context_description = fields.Text(compute="_compute_eval_context_description")

    common_code = fields.Text(
        "Common Code",
        help="""
        A place for helpers and constants.

        You can add here a function or variable, that don't start with underscore and then reuse it in task's code.
    """,
    )
    param_ids = fields.One2many("sync.project.param", "project_id", copy=True)
    text_param_ids = fields.One2many("sync.project.text", "project_id", copy=True)
    secret_ids = fields.One2many("sync.project.secret", "project_id", copy=True)
    task_ids = fields.One2many("sync.task", "project_id", copy=True)
    task_count = fields.Integer(compute="_compute_task_count")
    trigger_cron_count = fields.Integer(
        compute="_compute_triggers", help="Enabled Crons"
    )
    trigger_automation_count = fields.Integer(
        compute="_compute_triggers", help="Enabled DB Triggers"
    )
    trigger_webhook_count = fields.Integer(
        compute="_compute_triggers", help="Enabled Webhooks"
    )
    trigger_button_count = fields.Integer(
        compute="_compute_triggers", help="Manual Triggers"
    )
    trigger_button_ids = fields.Many2many(
        "sync.trigger.button", compute="_compute_triggers", string="Manual Triggers"
    )
    job_ids = fields.One2many("sync.job", "project_id")
    job_count = fields.Integer(compute="_compute_job_count")
    log_ids = fields.One2many("ir.logging", "sync_project_id")
    log_count = fields.Integer(compute="_compute_log_count")

    def copy(self, default=None):
        default = dict(default or {})
        default["active"] = False
        return super(SyncProject, self).copy(default)

    def _compute_eval_context_description(self):
        for r in self:
            if not r.eval_context:
                r.eval_context_description = ""
                continue
            method = getattr(self, EVAL_CONTEXT_PREFIX + r.eval_context)
            r.eval_context_description = method.__doc__

    def _compute_network_access_readonly(self):
        for r in self:
            r.network_access_readonly = r.sudo().network_access

    @api.depends("task_ids")
    def _compute_task_count(self):
        for r in self:
            r.task_count = len(r.with_context(active_test=False).task_ids)

    @api.depends("job_ids")
    def _compute_job_count(self):
        for r in self:
            r.job_count = len(r.job_ids)

    @api.depends("log_ids")
    def _compute_log_count(self):
        for r in self:
            r.log_count = len(r.log_ids)

    def _compute_triggers(self):
        for r in self:
            r.trigger_cron_count = len(r.mapped("task_ids.cron_ids"))
            r.trigger_automation_count = len(r.mapped("task_ids.automation_ids"))
            r.trigger_webhook_count = len(r.mapped("task_ids.webhook_ids"))
            r.trigger_button_count = len(r.mapped("task_ids.button_ids"))
            r.trigger_button_ids = r.mapped("task_ids.button_ids")

    @api.constrains("common_code")
    def _check_python_code(self):
        for r in self.sudo().filtered("common_code"):
            msg = test_python_expr(expr=(r.common_code or "").strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    def _get_log_function(self, job, function):
        self.ensure_one()

        def _log(cr, message, level, name, log_type):
            cr.execute(
                """
                INSERT INTO ir_logging(create_date, create_uid, type, dbname, name, level, message, path, line, func, sync_job_id)
                VALUES (NOW() at time zone 'UTC', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    self.env.uid,
                    log_type,
                    self._cr.dbname,
                    name,
                    level,
                    message,
                    "sync.job",
                    job.id,
                    function,
                    job.id,
                ),
            )

        def log(message, level=LOG_INFO, name=DEFAULT_LOG_NAME, log_type="server"):
            if self.env.context.get("new_cursor_logs") is False:
                return _log(self.env.cr, message, level, name, log_type)

            with self.env.registry.cursor() as cr:
                return _log(cr, message, level, name, log_type)

        return log

    def _get_eval_context(self, job, log):
        """Executed Secret and Common codes and return "exported" variables and functions"""
        self.ensure_one()
        log("Job started", LOG_DEBUG)
        start_time = time.time()

        def add_job(function, **options):
            if callable(function):
                function = function.__name__

            def f(*args, **kwargs):
                sub_job = self.env["sync.job"].create(
                    {"parent_job_id": job.id, "function": function}
                )
                queue_job = job.task_id.with_delay(**options).run(
                    sub_job, function, args, kwargs
                )
                sub_job.queue_job_id = queue_job.db_record()
                log(
                    "add_job: %s(*%s, **%s). See %s"
                    % (function, args, kwargs, sub_job),
                    level=LOG_INFO,
                )

            return f

        params = AttrDict()
        for p in self.param_ids:
            params[p.key] = p.value

        texts = AttrDict()
        for p in self.text_param_ids:
            texts[p.key] = p.value

        webhooks = AttrDict()
        for w in self.task_ids.mapped("webhook_ids"):
            webhooks[w.trigger_name] = w.website_url

        def log_transmission(recipient_str, data_str):
            log(data_str, name=recipient_str, log_type="data_out")

        def safe_getattr(o, k, d=None):
            if k.startswith("_"):
                raise ValidationError(_("You cannot use %s with getattr") % k)
            return getattr(o, k, d)

        def safe_setattr(o, k, v):
            if k.startswith("_"):
                raise ValidationError(_("You cannot use %s with setattr") % k)
            return setattr(o, k, v)

        def type2str(obj):
            return "%s" % type(obj)

        context = dict(self.env.context, log_function=log)
        env = self.env(context=context)
        link_functions = env["sync.link"]._get_eval_context()
        eval_context = dict(
            **link_functions,
            **self._get_sync_functions(log, link_functions),
            **{
                "env": env,
                "log": log,
                "log_transmission": log_transmission,
                "LOG_DEBUG": LOG_DEBUG,
                "LOG_INFO": LOG_INFO,
                "LOG_WARNING": LOG_WARNING,
                "LOG_ERROR": LOG_ERROR,
                "LOG_CRITICAL": LOG_CRITICAL,
                "params": params,
                "texts": texts,
                "webhooks": webhooks,
                "user": self.env.user,
                "trigger": job.trigger_name,
                "add_job": add_job,
                "json": json,
                "UserError": UserError,
                "ValidationError": ValidationError,
                "OSError": OSError,
                "RetryableJobError": RetryableJobError,
                "getattr": safe_getattr,
                "setattr": safe_setattr,
                "time": time,
                "datetime": datetime,
                "dateutil": dateutil,
                "timezone": timezone,
                "b64encode": base64.b64encode,
                "b64decode": base64.b64decode,
                "type2str": type2str,
                "DEFAULT_SERVER_DATETIME_FORMAT": DEFAULT_SERVER_DATETIME_FORMAT,
            }
        )
        reading_time = time.time() - start_time

        executing_custom_context = 0
        if self.eval_context:
            start_time = time.time()

            secrets = AttrDict()
            for p in self.sudo().secret_ids:
                secrets[p.key] = p.value
            eval_context_frozen = frozendict(eval_context)
            method = getattr(self, EVAL_CONTEXT_PREFIX + self.eval_context)
            eval_context = dict(**eval_context, **method(secrets, eval_context_frozen))
            cleanup_eval_context(eval_context)

            executing_custom_context = time.time() - start_time

        start_time = time.time()
        safe_eval(
            (self.common_code or "").strip(), eval_context, mode="exec", nocopy=True
        )
        executing_common_code = time.time() - start_time
        log(
            "Evalution context is prepared. Reading project data: %05.3f sec; preparing custom evalution context: %05.3f sec; Executing Common Code: %05.3f sec"
            % (reading_time, executing_custom_context, executing_common_code),
            LOG_DEBUG,
        )
        cleanup_eval_context(eval_context)
        return eval_context

    def _get_sync_functions(self, log, link_functions):
        def _sync(src_list, src2dst, link_src_dst, create=None, update=None):
            # * src_list: iterator of src_data
            # * src2dst: src_data -> dst_ref
            # * link_src_dst: links pair (src_data, dst_ref)
            # * create(src_data) -> dst_ref
            # * update(dst_ref, src_data)
            for src_data in src_list:
                dst_ref = src2dst(src_data)
                if dst_ref and update:
                    update(dst_ref, src_data)
                elif not dst_ref and create:
                    dst_ref = create(src_data)
                    link_src_dst(src_data, dst_ref)
                elif dst_ref:
                    log("Destination record already exists: %s" % dst_ref, LOG_DEBUG)
                elif not dst_ref:
                    log("Destination record not found for %s" % src_data, LOG_DEBUG)

        def sync_odoo2x(src_list, sync_info, create=False, update=False):
            # sync_info["relation"]
            # sync_info["x"]["update"]: (external_ref, odoo_record)
            # sync_info["x"]["create"]: odoo_record -> external_ref
            relation = sync_info["relation"]

            def _odoo2external(odoo_record):
                link = odoo_record.search_links(relation)
                return link.external

            def _add_link(odoo_record, external):
                odoo_record.set_link(relation, external)

            return _sync(
                src_list,
                _odoo2external,
                _add_link,
                create and sync_info["x"]["create"],
                update and sync_info["x"]["update"],
            )

        def sync_x2odoo(src_list, sync_info, create=False, update=False):
            # sync_info["relation"]
            # sync_info["x"]["get_ref"]
            # sync_info["odoo"]["update"]: (odoo_record, x)
            # sync_info["odoo"]["create"]: x -> odoo_record
            relation = sync_info["relation"]
            x2ref = sync_info["x"]["get_ref"]

            def _x2odoo(x):
                ref = x2ref(x)
                link = link_functions["get_link"](relation, ref)
                return link.odoo

            def _add_link(x, odoo_record):
                ref = x2ref(x)
                link = odoo_record.set_link(relation, ref)
                return link

            return _sync(
                src_list,
                _x2odoo,
                _add_link,
                create and sync_info["odoo"]["create"],
                update and sync_info["odoo"]["update"],
            )

        # def sync_x2y(src_list, sync_info, create=False, update=False):
        #     return sync_external(src_list, sync_info["relation"], sync_info["x"], sync_info["y"], create=create, update=update)
        # def sync_y2x(src_list, sync_info, create=False, update=False):
        #     return sync_external(src_list, sync_info["relation"], sync_info["y"], sync_info["x"], create=create, update=update)
        def sync_external(
            src_list, relation, src_info, dst_info, create=False, update=False
        ):
            # src_info["get_ref"]
            # src_info["system"]: e.g. "github"
            # src_info["update"]: (dst_ref, src_data)
            # src_info["create"]: src_data -> dst_ref
            # dst_info["system"]: e.g. "trello"
            def src2dst(src_data):
                src_ref = src_info["get_ref"](src_data)
                refs = {src_info["system"]: src_ref, dst_info["system"]: None}
                link = link_functions["get_link"](relation, refs)
                res = link.get(dst_info["system"])
                if len(res) == 1:
                    return res[0]

            def link_src_dst(src_data, dst_ref):
                src_ref = src_info["get_ref"](src_data)
                refs = {src_info["system"]: src_ref, dst_info["system"]: dst_ref}
                return link_functions["set_link"](relation, refs)

            return _sync(
                src_list,
                src2dst,
                link_src_dst,
                create and src_info["odoo"]["create_odoo"],
                update and src_info["odoo"]["update_odoo"],
            )

        return {
            "sync_odoo2x": sync_odoo2x,
            "sync_x2odoo": sync_x2odoo,
            "sync_external": sync_external,
        }


class SyncProjectParamMixin(models.AbstractModel):

    _name = "sync.project.param.mixin"
    _description = "Template model for Parameters"
    _rec_name = "key"

    key = fields.Char("Key", required=True)
    value = fields.Char("Value")
    description = fields.Char("Description", translate=True)
    url = fields.Char("Documentation")
    project_id = fields.Many2one("sync.project", ondelete="cascade")

    _sql_constraints = [("key_uniq", "unique (project_id, key)", "Key must be unique.")]


class SyncProjectParam(models.Model):

    _name = "sync.project.param"
    _description = "Project Parameter"
    _inherit = "sync.project.param.mixin"


class SyncProjectText(models.Model):
    _name = "sync.project.text"
    _description = "Project Text Parameter"
    _inherit = "sync.project.param.mixin"

    value = fields.Text("Value", translate=True)


class SyncProjectSecret(models.Model):

    _name = "sync.project.secret"
    _description = "Project Secret Parameter"
    _inherit = "sync.project.param.mixin"

    value = fields.Char(groups="sync.sync_group_manager")


# see https://stackoverflow.com/a/14620633/222675
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
