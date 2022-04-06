import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # Convert eval_context selection values into sync.project.context records
    # Copy eval_context values into eval_contexts
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _logger.info("Copying eval_context selection values into sync.project.context records")
        env['ir.model.fields.selection']._update_sync_project_context()
        sync_projects = env['sync.project'].with_context(active_test=False).search([])
        for sync_project in sync_projects:
            if not sync_project.eval_context:
                continue
            sync_project_context = env['sync.project.context'].search(
                [('name', '=', sync_project.eval_context)],
                limit=1
            )
            if not sync_project_context:
                continue
            sync_project.write({
                'eval_contexts': [(6, 0, sync_project_context.ids)],
            })
