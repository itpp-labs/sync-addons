from odoo import api, fields, models

RECORD_MAPPING_LINK_PREFIX = 'record_mappings_sync_project_'


class SyncLink(models.Model):
    _inherit = "sync.link"

    sync_project_id = fields.Many2one(
        'sync.project',
        compute='_compute_sync_project_id',
        inverse='_inverse_sync_project_id'
    )

    @api.depends('relation')
    def _compute_sync_project_id(self):
        """ Matches the sync project record based on the relation field """
        for record in self:
            if not record.relation or not record.relation.startswith(RECORD_MAPPING_LINK_PREFIX):
                record.sync_project_id = False
                continue
            sync_project_id = self.env['sync.project'].search(
                [
                    ('id', '=', int(record.relation[len(RECORD_MAPPING_LINK_PREFIX):])),
                    ('active', 'in', [True, False])
                ],
                limit=1
            )
            if sync_project_id:
                record.sync_project_id = sync_project_id
            else:
                record.sync_project_id = False

    @api.onchange('sync_project_id')
    def _onchange_sync_project_id(self):
        """ Sets the relation field value when the user chooses a sync project via the dropdown """
        if self.sync_project_id:
            self.relation = "%s%s" % (RECORD_MAPPING_LINK_PREFIX, self.sync_project_id.id)

    def _inverse_sync_project_id(self):
        """ Nothing to do in this case, but it's required for the field to work """
        return
