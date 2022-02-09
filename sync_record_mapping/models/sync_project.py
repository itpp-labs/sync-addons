from odoo import api, fields, models


class SyncProject(models.Model):
    _inherit = "sync.project"

    def _compute_record_mapping_relation(self):
        """ The relation is a computed unique string to allow assigning links to a particular project """
        for record in self:
            record.record_mapping_relation = "record_mappings_sync_project_%s" % record.id

    @staticmethod
    def record_mapping_domain(relation):
        return [
            '&',
            ('system2', '=', '__odoo__'),
            ('relation', '=', relation)
        ]

    record_mapping_relation = fields.Char(compute=_compute_record_mapping_relation, copy=False)

    def _compute_record_mapping_ids(self):
        for project in self:
            record_mapping_ids = self.env['sync.link'].search(
                self.record_mapping_domain(project.record_mapping_relation)
            )
            if record_mapping_ids:
                project.record_mapping_ids = [(6, 0, record_mapping_ids.ids)]
            else:
                project.record_mapping_ids = False

    def _inverse_record_mapping_ids(self):
        """ Detects changes in record mappings to delete the records """
        for project in self:
            record_mapping_ids = self.env['sync.link'].search(
                self.record_mapping_domain(project.record_mapping_relation)
            )
            record_mapping_ids_to_delete = record_mapping_ids - project.record_mapping_ids
            if record_mapping_ids_to_delete:
                record_mapping_ids_to_delete.unlink()

    record_mapping_ids = fields.Many2many(
        'sync.link',
        compute='_compute_record_mapping_ids',
        inverse='_inverse_record_mapping_ids',
        copy=False
    )