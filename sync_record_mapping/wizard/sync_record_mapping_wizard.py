from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SyncRecordMappingWizard(models.TransientModel):
    _name = 'sync.record.mapping.wizard'

    res_model = fields.Char('Odoo Model')
    res_id = fields.Many2oneReference('Related Document ID', model_field='res_model')

    @staticmethod
    def record_mapping_domain(res_id, res_model):
        return [
            '&',
            '&',
            ('system2', '=', '__odoo__'),
            ('ref2', '=', str(res_id)),
            ('model', '=', res_model)
        ]

    @api.depends('res_model', 'res_id')
    def _compute_record_mapping_ids(self):
        self.ensure_one()
        if not self.res_model or not self.res_id:
            raise UserError(_('Invalid model or record.'))
        record_mapping_ids = self.env['sync.link'].search(
            self.record_mapping_domain(self.res_id, self.res_model)
        )
        if record_mapping_ids:
            self.record_mapping_ids = [(6, 0, record_mapping_ids.ids)]
        else:
            self.record_mapping_ids = False

    def _inverse_record_mapping_ids(self):
        """ Detects changes in record mappings to delete the records """
        self.ensure_one()
        record_mapping_ids = self.env['sync.link'].search(
            self.record_mapping_domain(self.res_id, self.res_model)
        )
        # TODO: Could this possibly cause a race condition?
        record_mapping_ids_to_delete = record_mapping_ids - self.record_mapping_ids
        if record_mapping_ids_to_delete:
            record_mapping_ids_to_delete.unlink()

    record_mapping_ids = fields.Many2many(
        'sync.link',
        compute='_compute_record_mapping_ids',
        inverse='_inverse_record_mapping_ids',
        store=True
    )