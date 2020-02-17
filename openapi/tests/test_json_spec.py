# Copyright 2018-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
# License MIT (https://opensource.org/licenses/MIT).
import json

from odoo.tests.common import HttpCase, PORT
from bravado_core.spec import Spec
from swagger_spec_validator import SwaggerValidationError
from odoo.tests import tagged


@tagged('post_install', 'at_install')
class TestJsonSpec(HttpCase):

    def test_json_base(self):

        resp = self.url_open("http://localhost:%d/api/v1/demo/swagger.json?token=demo_token&download" % PORT,
                             timeout=30)
        self.assertEqual(resp.status_code, 200, 'Cannot get json spec')
        # TODO add checking  actual content of the json

    def test_OAS_scheme_for_demo_data_is_valid(self):
        resp = self.url_open("http://localhost:%d/api/v1/demo/swagger.json?token=demo_token&download" % PORT,
                             timeout=30)
        spec_dict = json.loads(resp.content.decode('utf8'))
        try:
            Spec.from_dict(spec_dict, config={'validate_swagger_spec': True})
        except SwaggerValidationError as e:
            self.fail('A JSON Schema for Swagger 2.0 is not valid:\n %s' % e)
