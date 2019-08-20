# -*- coding: utf-8 -*-
# Copyright 2018-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import json

import requests
import logging

from odoo import api
from odoo.tests.common import HttpCase, PORT, get_db_name

from ..controllers import pinguin

_logger = logging.getLogger(__name__)

USER_DEMO = 'base.user_demo'
USER_ADMIN = 'base.user_root'


class TestAPI(HttpCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestAPI, self).setUp()
        self.db_name = get_db_name()
        self.phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
        self.demo_user = self.phantom_env.ref(USER_DEMO)
        self.admin_user = self.phantom_env.ref(USER_ADMIN)

    def request(self, method, url, auth=None, **kwargs):
        kwargs.setdefault('model', 'res.partner')
        kwargs.setdefault('namespace', 'demo')
        url = ("http://localhost:%d/api/v1/{namespace}" % PORT + url).format(**kwargs)
        #return self.url_open(url)
        self.opener = requests.Session()
        self.opener.cookies['session_id'] = self.session_id
        return self.opener.request(method, url, timeout=30, auth=auth)

    def request_from_user(self, user, *args, **kwargs):
        kwargs['auth'] = requests.auth.HTTPBasicAuth(self.db_name, user.openapi_token)
        return self.request(*args, **kwargs)

    def test_read_many_all(self):
        resp = self.request_from_user(self.demo_user, 'GET', '/{model}')
        self.assertEqual(resp.status_code, pinguin.CODE__success)
        # TODO check content

    # def _test_read_many_domain(self):
    #     resp = self.request_from_self.demo_user('GET', 'demo', 'res.partner', params = {'domain': '[("phone", "!=", False)]'})
    #     self.assertEqual(resp.status_code, 200)
    #     # TODO check content

    def _test_read_one(self):
        record_id = self.phantom_env[model_name].search([], limit=1).id
        resp = self.request_from_user('GET', model_name, record_id, user=self.demo_user)
        self.assertEqual(resp.status_code, pinguin.CODE__success)
        # TODO check content

    def _test_create_one(self):
        data_for_create = {
            'name': 'created_from_test',
            'type': 'other'
        }
        resp = self.request_from_user('POST', model_name, data=data_for_create, user=self.demo_user)
        self.assertEqual(resp.status_code, pinguin.CODE__created)
        created_user = self.phantom_env[model_name].browse(resp.json()['id'])
        self.assertEqual(created_user.name, data_for_create['name'])

    # disabled because there is one cursor in the tests, and to create a log in case of an error, you need two cursors
    # def _test_create_one_with_invalid_data(self):
    #     self.phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
    #     namespace_name = 'demo'
    #     model_name = 'res.partner'
    #     data_for_create = {'company_id': 0, 'name': 'string', 'email': 'string'}
    #     self.demo_user = self.phantom_env.ref(USER_DEMO)
    #     resp = self.request_from_user('POST', model_name, data=data_for_create, user=self.demo_user)
    #     self.assertEqual(resp.status_code, 400)

    def _test_update_one(self):
        data_for_update = {
            'name': 'for update in test',
        }
        partner = self.phantom_env[model_name].search([], limit=1)
        resp = self.request_from_user('PUT', model_name, partner.id, data=data_for_update, user=self.demo_user)
        self.assertEqual(resp.status_code, pinguin.CODE__ok_no_content)
        self.assertEqual(partner.name, data_for_update['name'])

    def _test_unlink_one(self):
        partner = self.phantom_env[model_name].create({'name': 'record for deleting from test'})
        resp = self.request_from_user('DELETE', model_name, partner.id, user=self.demo_user)
        self.assertEqual(resp.status_code, pinguin.CODE__ok_no_content)
        self.assertFalse(self.phantom_env[model_name].browse(partner.id).exists())

    def _test_unauthorized_user(self):
        resp = self.request('GET', model_name)
        self.assertEqual(resp.status_code, pinguin.CODE__no_user_auth[0])

    def _test_invalid_dbname(self):
        db_name = 'invalid_db_name'
        resp = self.request('GET', model_name, auth=requests.auth.HTTPBasicAuth(db_name, self.demo_user.openapi_token))
        self.assertEqual(resp.status_code, pinguin.CODE__db_not_found[0])
        self.assertEqual(resp.json()['error'], pinguin.CODE__db_not_found[1])

    def _test_invalid_user_token(self):
        invalid_token = 'invalid_user_token'
        resp = self.request('GET', model_name, auth=requests.auth.HTTPBasicAuth(self.db_name, invalid_token))
        self.assertEqual(resp.status_code, pinguin.CODE__no_user_auth[0])
        self.assertEqual(resp.json()['error'], pinguin.CODE__no_user_auth[1])

    def _test_user_not_allowed_for_namespace(self):
        namespace = self.phantom_env['openapi.namespace'].search([('name', '=')])
        new_user = self.phantom_env['res.users'].create({
            'name': 'new user',
            'login': 'new_user',
        })
        new_user.reset_openapi_token()
        self.assertTrue(new_user.id not in namespace.user_ids.ids)
        self.assertTrue(namespace.id not in new_user.namespace_ids.ids)

        resp = self.request_from_user('GET', model_name, user=new_user)
        self.assertEqual(resp.status_code, pinguin.CODE__user_no_perm[0], resp.json())
        self.assertEqual(resp.json()['error'], pinguin.CODE__user_no_perm[1])

    def _test_call_allowed_method_on_singleton_record(self):
        partner = self.phantom_env[model_name].search([], limit=1)

        method_params = {
            'vals': {
                'name': 'changed from write method which call from api'
            }
        }
        data = {
            'method_name': 'write',
            'method_params': json.dumps(method_params)
        }

        resp = self.request_from_user('PATCH', model_name, partner.id, data=data, user=self.demo_user)

        self.assertEqual(resp.status_code, pinguin.CODE__success)
        self.assertTrue(resp.json())
        self.assertEqual(partner.name, method_params['vals']['name'])

    def _test_call_allowed_method_on_recordset(self):

        partners = self.phantom_env[model_name].search([], limit=5)
        method_params = {
            'vals': {
                'name': 'changed from write method which call from api'
            },
        }
        data = {
            'method_name': 'write',
            'ids': json.dumps(partners.mapped('id')),
            'method_params': json.dumps(method_params)
        }

        resp = self.request_from_user('PATCH', model_name, data=data, user=self.demo_user)

        self.assertEqual(resp.status_code, pinguin.CODE__success)
        for i in range(len(partners)):
            self.assertTrue(resp.json()[i])
        for partner in partners:
            self.assertEqual(partner.name, method_params['vals']['name'])

    def _test_log_creating(self):
        logs_count_before_request = len(self.phantom_env['openapi.log'].search([]))
        self.request_from_user('GET', model_name, user=self.demo_user)
        logs_count_after_request = len(self.phantom_env['openapi.log'].search([]))
        self.assertTrue(logs_count_after_request > logs_count_before_request)

    def _test_get_report_for_allowed_model(self):
        super_user = self.phantom_env.ref(USER_ROOT)
        modelname_for_report = 'ir.module.module'
        report_external_id = 'base.ir_module_reference_print'

        model_for_report = self.phantom_env['ir.model'].search([('model', '=', modelname_for_report)])
        namespace = self.phantom_env['openapi.namespace'].search([('name', '=')])
        records_for_report = self.phantom_env[modelname_for_report].search([], limit=3)
        docids = ','.join([str(i) for i in records_for_report.ids])

        self.phantom_env['openapi.access'].create({
            'active': True,
            'namespace_id': namespace.id,
            'model_id': model_for_report.id,
            'model': modelname_for_report,
            'api_create': False,
            'api_read': True,
            'api_update': False,
            'api_public_methods': False,
            'public_methods': False,
            'private_methods': False,
            'read_one_id': False,
            'read_many_id': False,
            'create_context_ids': False
        })

        super_user.write({
            'namespace_ids': [(4, namespace.id)]
        })

        url = "http://localhost:%d/api/v1/%s/report/html/%s/%s" % (PORT, report_external_id, docids)
        resp = requests.request('GET', url, timeout=30, auth=requests.auth.HTTPBasicAuth(self.db_name, super_user.openapi_token))
        self.assertEqual(resp.status_code, pinguin.CODE__success)
