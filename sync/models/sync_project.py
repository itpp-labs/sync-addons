# Copyright 2020,2022,2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020-2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

import base64
import logging
import os
from datetime import datetime

import urllib3
from pytz import timezone

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, html2plaintext
from odoo.tools.misc import get_lang
from odoo.tools.safe_eval import (
    datetime as safe_datetime,
    dateutil,
    json,
    safe_eval,
    test_python_expr,
    time,
)
from odoo.tools.translate import _

from odoo.addons.queue_job.exception import RetryableJobError

from ..lib.tools.safe_eval import safe_eval__MAGIC, test_python_expr__MAGIC
from ..tools import (
    AttrDict,
    add_items,
    compile_markdown_to_html,
    convert_python_front_matter_to_comment,
    extract_yaml_from_markdown,
    extract_yaml_from_python,
    fetch_gist_data,
    has_function_defined,
    url2base64,
    url2bin,
)
from .ir_logging import LOG_CRITICAL, LOG_DEBUG, LOG_ERROR, LOG_INFO, LOG_WARNING

_logger = logging.getLogger(__name__)
DEFAULT_LOG_NAME = "Log"


def eval_export(eval_function, code, eval_context):
    EXPORT = {}

    def export(*args, **kwargs):
        # Используем общую функцию для добавления элементов в EXPORT
        add_items(EXPORT, *args, **kwargs)

    eval_context = dict(eval_context, export=export)
    eval_function((code or "").strip(), eval_context, mode="exec", nocopy=True)
    return AttrDict(EXPORT)


class SyncProject(models.Model):

    _name = "sync.project"
    _description = "Sync Project"

    name = fields.Char(
        "Name",
        help="e.g. Legacy Migration or eCommerce Integration",
    )
    active = fields.Boolean(default=False)

    source_url = fields.Char(
        "Source",
        help="Paste link to gist page, e.g. https://gist.github.com/yelizariev/e0585a0817c4d87b65b8a3d945da7ca2",
    )
    source_updated_at = fields.Datetime("Version", readonly=True)
    description = fields.Html(readonly=True)

    core_code = fields.Text(string="Core Code", readonly=True)
    common_code = fields.Text("Project Library Code")

    param_ids = fields.One2many(
        "sync.project.param", "project_id", copy=True, string="Parameters"
    )
    param_description = fields.Html(readonly=True)

    text_param_ids = fields.One2many(
        "sync.project.text", "project_id", copy=True, string="Templates"
    )
    text_param_description = fields.Html(readonly=True)

    secret_ids = fields.One2many("sync.project.secret", "project_id", copy=True)
    secret_description = fields.Html(readonly=True)

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
    job_ids = fields.One2many("sync.job", "project_id")
    job_count = fields.Integer(compute="_compute_job_count")
    log_ids = fields.One2many("ir.logging", "sync_project_id")
    log_count = fields.Integer(compute="_compute_log_count")
    link_ids = fields.One2many("sync.link", "project_id")
    link_count = fields.Integer(compute="_compute_link_count")
    data_ids = fields.One2many("sync.data", "project_id")

    def copy(self, default=None):
        default = dict(default or {})
        default["active"] = False
        return super(SyncProject, self).copy(default)

    def unlink(self):
        self.with_context(active_test=False).mapped("task_ids").unlink()
        return super().unlink()

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

    @api.depends("link_ids")
    def _compute_link_count(self):
        for r in self:
            r.link_count = len(r.link_ids)

    def _compute_triggers(self):
        for r in self:
            r.trigger_cron_count = len(r.mapped("task_ids.cron_ids"))
            r.trigger_automation_count = len(r.mapped("task_ids.automation_ids"))
            r.trigger_webhook_count = len(r.mapped("task_ids.webhook_ids"))

    @api.constrains("common_code")
    def _check_python_common_code(self):
        for r in self.sudo().filtered("common_code"):
            msg = test_python_expr(expr=(r.common_code or "").strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    @api.constrains("core_code")
    def _check_python_core_code(self):
        for r in self.sudo().filtered("core_code"):
            msg = test_python_expr__MAGIC(expr=(r.core_code or "").strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    def write(self, vals):
        if "core_code" in vals and not self.env.user.has_group(
            "sync.sync_group_manager"
        ):
            raise AccessError(_("Only Administrator can update the Core Code."))

        return super().write(vals)

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
        """Prepare Task Evaluation Context"""
        self.ensure_one()
        log("Let's prepare Evaluation Context", LOG_DEBUG)

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

        def record2image(record, fname="image_1920"):
            return (
                record.sudo()
                .env["ir.attachment"]
                .search(
                    [
                        ("res_model", "=", record._name),
                        ("res_field", "=", fname),
                        ("res_id", "=", record.id),
                    ],
                    limit=1,
                )
            )

        context = dict(self.env.context, log_function=log, sync_project_id=self.id)
        env = self.env(context=context)
        link_functions = env["sync.link"]._get_eval_context()
        MAGIC = AttrDict(
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
                "get_lang": get_lang,
                "url2base64": url2base64,
                "url2bin": url2bin,
                "html2plaintext": html2plaintext,
                "time": time,
                "datetime": safe_datetime,
                "dateutil": dateutil,
                "timezone": timezone,
                "b64encode": base64.b64encode,
                "b64decode": base64.b64decode,
                "type2str": type2str,
                "record2image": record2image,
                "DEFAULT_SERVER_DATETIME_FORMAT": DEFAULT_SERVER_DATETIME_FORMAT,
                "AttrDict": AttrDict,
            },
        )
        SECRETS = AttrDict()
        for p in self.secret_ids:
            SECRETS[p.key] = p.value

        PARAMS = AttrDict()
        for p in self.param_ids:
            PARAMS[p.key] = p.value

        for p in self.text_param_ids:
            if p.key in PARAMS:
                raise ValidationError(
                    _(
                        "Project Templates and Settings should not have parameters with the same key: %s"
                    )
                    % p.key
                )
            PARAMS[p.key] = p.value

        WEBHOOKS = AttrDict()
        for w in self.task_ids.mapped("webhook_ids"):
            WEBHOOKS[w.trigger_name] = w.website_url

        DATA = AttrDict()
        for d in self.data_ids:
            DATA[d.name] = d

        core_eval_context = {
            "MAGIC": MAGIC,
            "SECRETS": SECRETS,
        }
        CORE = eval_export(safe_eval__MAGIC, self.core_code, core_eval_context)

        lib_eval_context = {
            "MAGIC": MAGIC,
            "CORE": CORE,
            "PARAMS": PARAMS,
            "WEBHOOKS": WEBHOOKS,
            "DATA": DATA,
        }
        LIB = eval_export(safe_eval, self.common_code, lib_eval_context)

        task_eval_context = dict(lib_eval_context, LIB=LIB)
        log("Evaluation Context is ready!", LOG_DEBUG)
        return task_eval_context

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

    def magic_upgrade(self):
        self.ensure_one()
        if not self.source_url:
            raise UserError(_("Please provide url to the gist page"))

        gist_content = fetch_gist_data(self.source_url)
        gist_files = {}
        for file_name, file_info in gist_content["files"].items():
            gist_files[file_name] = file_info["content"]

        vals = {}

        if not self.name:
            vals["name"] = gist_content.get("description", "Sync 🪬 Studio")

        vals["source_updated_at"] = datetime.strptime(
            gist_content.get("updated_at"), "%Y-%m-%dT%H:%M:%SZ"
        )

        # [Documentation]
        vals["description"] = (
            compile_markdown_to_html(gist_files.get("README.md"))
            if gist_files.get("README.md")
            else "<h1>Please add README.md file to place some documentation here</h1>"
        )

        # [PARAMS] and [SECRETS]
        for model, field_name, file_name in (
            ("sync.project.param", "param_description", "settings.markdown"),
            (
                "sync.project.text",
                "text_param_description",
                "settings.templates.markdown",
            ),
            ("sync.project.secret", "secret_description", "settings.secrets.markdown"),
        ):
            file_content = gist_files.get(file_name)
            if not file_content:
                continue
            vals[field_name] = compile_markdown_to_html(file_content)
            meta = extract_yaml_from_markdown(file_content)

            for key, initial_value in meta.items():
                param_vals = {
                    "key": key,
                    "initial_value": initial_value,
                    "project_id": self.id,
                }
                self.env[model]._create_or_update_by_xmlid(
                    param_vals, f"PARAM_{key}", namespace=self.id
                )

        # [CORE] and [LIB]
        for field_name, file_name in (
            ("core_code", "core.py"),
            ("common_code", "library.py"),
        ):
            if gist_files.get(file_name):
                vals[field_name] = gist_files[file_name]

        # [DATA]
        http = urllib3.PoolManager()
        for file_info in gist_content["files"].values():
            # e.g. "data.emoji.csv"
            file_name = file_info["filename"]
            if not file_name.startswith("data."):
                continue
            raw_url = file_info["raw_url"]
            response = http.request("GET", raw_url)
            if response.status == 200:
                file_content = response.data
                file_content = base64.b64encode(file_content)
            else:
                raise Exception(
                    f"Failed to fetch raw content from {raw_url}. Status code: {response.status}"
                )

            technical_name = file_name
            technical_name = technical_name[len("data.") :]
            technical_name = os.path.splitext(technical_name)[0]
            technical_name = technical_name.replace(".", "_")

            data_vals = {
                "name": technical_name,
                "project_id": self.id,
                "file_name": file_name,
                "file_content": file_content,
            }
            self.env["sync.data"]._create_or_update_by_xmlid(
                data_vals, file_name, namespace=self.id
            )

        # Tasks 🦋
        for file_name in gist_files:
            # e.g. "task.setup.py"
            if not (file_name.startswith("task.") and file_name.endswith(".py")):
                continue

            # e.g. "setup"
            task_technical_name = file_name[len("task.") : -len(".py")]

            # Process file content
            file_content = gist_files[file_name]
            meta = extract_yaml_from_python(file_content)
            task_name = meta.get("TITLE", f"<No TITLE found at the {file_name}>")

            # Update code to bypass security checks
            file_content = convert_python_front_matter_to_comment(file_content)

            # Check if code is valid
            syntax_errors = test_python_expr(file_content, mode="exec")
            if syntax_errors:
                raise ValueError(
                    f"Invalid python code at file {file_name}:\n\n{syntax_errors}"
                )

            # Check if python code has method `handle_button`
            has_handle_button = has_function_defined(file_content, "handle_button")

            task_vals = {
                "name": task_name,
                "code": file_content,
                "magic_button": meta.get("MAGIC_BUTTON", "Magic ✨ Button")
                if has_handle_button
                else None,
                "project_id": self.id,
            }
            task = self.env["sync.task"]._create_or_update_by_xmlid(
                task_vals, task_technical_name, namespace=self.id
            )

            def create_trigger(model, data):
                vals = dict(
                    {key: value for key, value in data.items() if value is not None},
                    sync_task_id=task.id,
                    trigger_name=data["name"],
                )
                return self.env[model]._create_or_update_by_xmlid(
                    vals, data["name"], namespace=self.id
                )

            # Create/Update triggers
            for data in meta.get("CRON", []):
                create_trigger("sync.trigger.cron", data)

            for data in meta.get("WEBHOOK", []):
                create_trigger("sync.trigger.webhook", data)

            for data in meta.get("DB_TRIGGERS", []):
                model_id = self.env["ir.model"]._get(data["model"]).id
                create_trigger(
                    "sync.trigger.automation", dict(data, model_id=model_id, model=None)
                )

        self.update(vals)


class SyncProjectParamMixin(models.AbstractModel):

    _name = "sync.project.param.mixin"
    _description = "Template model for Parameters"
    _rec_name = "key"

    key = fields.Char("Key", required=True)
    value = fields.Char("Value")
    initial_value = fields.Char(
        compute="_compute_initial_value",
        inverse="_inverse_initial_value",
        help="A virtual field that, during writing, stores the value in the value field, but only if it is empty. \
             It's used during module upgrade to prevent overwriting parameter values. ",
    )
    project_id = fields.Many2one("sync.project", ondelete="cascade")

    # Deprecated fields to be deleted in v17+
    description = fields.Char("Description", translate=True)
    url = fields.Char("Documentation")

    _sql_constraints = [("key_uniq", "unique (project_id, key)", "Key must be unique.")]

    def _compute_initial_value(self):
        for r in self:
            r.initial_value = r.value

    def _inverse_initial_value(self):
        for r in self:
            if not r.value:
                r.value = r.initial_value


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

    def action_show_value(self):
        self.ensure_one()
        return {
            "name": _("Secret Parameter"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sync.project.secret",
            "target": "new",
            "res_id": self.id,
        }
