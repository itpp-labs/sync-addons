# _update_selection

from odoo import fields, models


class IrModelSelection(models.Model):
    _inherit = 'ir.model.fields.selection'

    def _reflect_selections(self, model_names):
        """
            Temporary compatibility helper for modules still using eval_context's selection_add.
            This field is being deprecated. Please create sync.project.context records instead.
            See data/sync_project_context.xml
        """
        res = super(IrModelSelection, self)._reflect_selections(model_names)
        eval_context_changed = [
            field
            for model_name in model_names
            for field_name, field in self.env[model_name]._fields.items()
            if model_name == 'sync.project'
            if field_name == 'eval_context'
        ]
        if eval_context_changed and 'sync.project.context' in self.env:
            spc = self.env['sync.project.context']
            many2many_values = spc.search([]).mapped(lambda v: v.name)
            new_selection_values = self.env['ir.model.fields.selection'].search(
                [('field_id.model', '=', 'sync.project'), ('field_id.name', '=', 'eval_context')]
            ).filtered(lambda v, vals=many2many_values: v.value not in vals)
            if new_selection_values:
                for new_selection_value in new_selection_values:
                    spc.create({
                        'name': new_selection_value.value,
                        'display_name': new_selection_value.name
                    })
        return res

