# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, fields, models


class SyncTriggerMixin(models.AbstractModel):

    _name = "sync.trigger.mixin"
    _description = "Mixing for trigger models"
    _rec_name = "trigger_name"

    trigger_name = fields.Char(
        "Trigger Name", help="Technical name to be used in task code", required=True
    )
    job_ids = fields.One2many("sync.job", "task_id")
    job_count = fields.Integer(compute="_compute_job_count")

    def _compute_job_count(self):
        for r in self:
            r.job_count = len(r.job_ids)

    def _update_name(self, vals):
        if not ("sync_task_id" in vals or "trigger_name" in vals):
            return
        if not self._fields["name"].required:
            return
        for record in self:
            if record.name != self._description:
                continue
            name = "Sync Studio: %s -> %s" % (
                record.sync_project_id.name,
                record.trigger_name,
            )
            record.write({"name": name})

    def write(self, vals):
        res = super().write(vals)
        self._update_name(vals)
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._update_name(vals)
        return res

    def default_get(self, fields):
        vals = super(SyncTriggerMixin, self).default_get(fields)
        # put model description in case if name is required field
        if self._fields["name"].required:
            vals["name"] = self._description
        return vals


class SyncTriggerMixinModelId(models.AbstractModel):

    _name = "sync.trigger.mixin.model_id"
    _description = "Mixing to fill model_id field"

    @api.model_create_multi
    def create(self, vals_list):
        model_id = self.env.ref("base.model_res_partner").id
        for vals in vals_list:
            vals.setdefault("model_id", model_id)
        return super(SyncTriggerMixinModelId, self).create(vals_list)


class SyncTriggerMixinActions(models.AbstractModel):

    _name = "sync.trigger.mixin.actions"
    _description = "Mixing for triggers that inherit actions"

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        vals["state"] = "code"
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for r in records:
            r.code = r.get_code()
        return records
