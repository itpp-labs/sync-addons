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
        if not hasattr(self, "sync_task_id"):
            return vals.get('name')
        return "Sync Studio [%s]: %s -> %s" % (
            self.sync_task_id.project_id.name,
            self.sync_task_id.name,
            vals.get('trigger_name', self.trigger_name)
        )

    def write(self, vals):
        for record in self:
            vals['name'] = record._update_name(vals)
            super(SyncTriggerMixin, record).write(vals)
        return True

    @api.model
    def create(self, vals):
        vals['name'] = self._update_name(vals)
        return super(SyncTriggerMixin, self).create(vals)

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
