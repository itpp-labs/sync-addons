# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

import json
import logging
import xmlrpc.client as _client

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.queue_job.exception import RetryableJobError
from odoo.addons.sync.tools import LogExternalQuery

_logger = logging.getLogger(__name__)


class SyncProjectOdoo2Odoo(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(
        selection_add=[
            ("odoo2odoo", "Odoo2odoo"),
        ],
        ondelete={"telegram": "cascade"},
    )

    @api.model
    def _eval_context_odoo2odoo(self, secrets, eval_context):
        """
        Additional functions to access external Odoo:

        * odoo_execute_kw(model, method, *args, **kwargs)
        * sync_odoo2odoo_push(model_name, domain=None, fields=None, active_test=True, create=False, update=False)
        * sync_odoo2odoo_pull(model_name, domain=None, fields=None, active_test=True, create=False, update=False)

            create: boolean value for "create record if it doesn't exist"
            update: boolean value for "update record if it exists"
            domain: which records of model_name to sync
            fields: which fields to sync
            active_test: value to pass to context on reading


        Connection is established according to following parameters:

        * params.URL
        * params.DB
        * secrets.USERNAME
        * secrets.PASSWORD
        """
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all([params.URL, params.DB, secrets.USERNAME, secrets.PASSWORD]):
            raise UserError(_("External Odoo Credentials are not set"))

        @LogExternalQuery("Odoo2Odoo->odoo_execute_kw", eval_context)
        def odoo_execute_kw(model, method, *args, **kwargs):
            url = params.URL
            if url.endswith("/"):
                url = url[:-1]
            log_transmission(
                "XMLRPC DB={} URL={}".format(params.DB, url),
                json.dumps([method, args, kwargs]),
            )
            try:
                common = _client.ServerProxy("{}/xmlrpc/2/common".format(url))
                uid = common.authenticate(
                    params.DB, secrets.USERNAME, secrets.PASSWORD, {}
                )
                models = _client.ServerProxy("{}/xmlrpc/2/object".format(url))
            except OSError:
                raise RetryableJobError("Error on connecting to external Odoo")
            res = models.execute_kw(
                params.DB, uid, secrets.PASSWORD, model, method, args, kwargs
            )
            log("Response: %s" % res, level="debug")
            return res

        def _partner2vals(partner, FIELDS):
            IMAGE_FIELD = "image_1920"
            res = {}
            for f in FIELDS:
                res[f] = getattr(partner, f)
            if res[IMAGE_FIELD]:
                res[IMAGE_FIELD] = res[IMAGE_FIELD].decode("utf-8")
            else:
                res[IMAGE_FIELD] = False
            return res

        def sync_odoo2odoo_push(
            model_name,
            domain=None,
            fields=None,
            active_test=True,
            create=False,
            update=False,
        ):
            REL = "sync_odoo2odoo:%s" % model_name

            log(
                "Push data: %s" % json.dumps([model_name, domain, active_test]),
                level="debug",
            )

            recs = (
                self.env[model_name]
                .with_context(active_test=active_test)
                .search(domain)
            )
            links = recs.search_links(REL)
            records_with_link = links.odoo
            records_without_link = recs - records_with_link

            if create:
                for r in records_without_link:
                    # create record on remote Odoo
                    fields_dict = _partner2vals(r, fields)
                    fields_dict["comment"] = "by Sync Studio"
                    external_id = odoo_execute_kw(model_name, "create", fields_dict)
                    r.set_link(REL, external_id)

                    log_transmission(
                        "Odoo2odoo->Push (Create)",
                        json.dumps([model_name, r, fields_dict]),
                    )

            # object already exists - update it
            if update:
                for r in records_with_link:
                    # update record on remote Odoo
                    fields_dict = _partner2vals(r, fields)
                    external_id = int(r.search_links(REL).external)
                    odoo_execute_kw(model_name, "write", external_id, fields_dict)

                    log_transmission(
                        "Odoo2odoo->Push (Update)",
                        json.dumps([model_name, r, fields_dict]),
                    )

        def sync_odoo2odoo_pull(
            model_name,
            domain=None,
            fields=None,
            active_test=True,
            create=False,
            update=False,
        ):
            REL = "sync_odoo2odoo:%s" % model_name

            log(
                "Pull data: %s" % json.dumps([model_name, domain, active_test]),
                level="debug",
            )

            external_recs = odoo_execute_kw(
                model_name,
                "search_read",
                domain=domain,
                fields=fields,
                context={"active_test": active_test},
            )
            external_recs = {d["id"]: d for d in external_recs}
            links = self.env[model_name].search_links(REL)
            external_recs_with_link = []
            # фикс если вдруг ссылка всего одна например 41, то рвньше разбивало на [4,1}
            for link in links:
                external_recs_with_link.append(int(link.external))
            log(" external_recs_with_link: %s" % external_recs_with_link, level="debug")
            external_recs_without_link = list(
                set(external_recs.keys()) - set(external_recs_with_link)
            )

            if create:
                # create record on local Odoo,  создает дубликаты если ссылка отсутсвует
                for er in external_recs_without_link:
                    fields_dict = external_recs[er]
                    fields_dict.pop("id")
                    fields_dict["comment"] = "by Sync Studio"
                    r = self.env[model_name].create(fields_dict)
                    r.set_link(REL, er)

                    log_transmission(
                        "Odoo2odoo->Push (Create)",
                        json.dumps([model_name, r, fields_dict]),
                    )

            if update:
                # update record on remote Odoo
                for er in external_recs_with_link:
                    fields_dict = {}
                    fields_dict = external_recs[er]
                    fields_dict.pop("id")
                    r = self.env["sync.link"]._get_link(REL, er).odoo
                    r.write(fields_dict)

                    log_transmission(
                        "Odoo2odoo->Push (Update)",
                        json.dumps([model_name, r, fields_dict]),
                    )

        return {
            "odoo_execute_kw": odoo_execute_kw,
            "sync_odoo2odoo_push": sync_odoo2odoo_push,
            "sync_odoo2odoo_pull": sync_odoo2odoo_pull,
        }
