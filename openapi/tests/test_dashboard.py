# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests.common import HttpCase
from odoo import api


class TestDashboard(HttpCase):
    at_install = True
    post_install = True

    def test_dashboard(self):

        phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        phantom_env['ir.module.module'].search(
            [('name', '=', 'openapi')],
            limit=1
        ).state = 'installed'

        # Grant Administrator access to demo user
        demo_user = phantom_env.ref('base.user_demo')
        demo_user.write({
            'groups_id': [(4, phantom_env.ref('base.group_system').id)],
        })
        # run as demo
        self.phantom_js(
            '/web',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('openapi_dashboard')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.openapi_dashboard.ready",

            login='demo'
        )
