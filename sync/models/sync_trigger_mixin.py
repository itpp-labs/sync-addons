# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2020 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, fields, models


class SyncTriggerMixin(models.AbstractModel):

    _name = "sync.trigger.mixin"
    _description = "Mixing for trigger models"
    _rec_name = "trigger_name"
    _default_name = None

    trigger_name = fields.Char(
        "Trigger Name", help="Technical name to be used in task code", required=True
    )
    job_ids = fields.One2many("sync.job", "task_id")
    job_count = fields.Integer(compute="_compute_job_count")

    def _compute_job_count(self):
        for r in self:
            r.job_count = len(r.job_ids)

    @api.model
    def default_get(self, fields):
        vals = super(SyncTriggerMixin, self).default_get(fields)
        if self._default_name:
            vals["name"] = self._default_name
        return vals

    def name_get(self):
        result = []
        for r in self:
            name = r.trigger_name
            if r.name and r.name != self._default_name:
                name += " " + r.name
            result.append((r.id, name))
        return result


class SyncTriggerMixinModelId(models.AbstractModel):

    _name = "sync.trigger.mixin.model_id"
    _description = "Mixing to fill model_id field"

    @api.model
    def create(self, vals):
        model_id = self.env.ref("base.model_res_partner").id
        vals.setdefault("model_id", model_id)
        return super(SyncTriggerMixinModelId, self).create(vals)


class SyncTriggerMixinActions(models.AbstractModel):

    _name = "sync.trigger.mixin.actions"
    _description = "Mixing for triggers that inherit actions"

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        vals["state"] = "code"
        return vals

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.code = record.get_code()
        return record
