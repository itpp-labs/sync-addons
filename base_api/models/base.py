# Copyright 2019,2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2019 Anvar Kildebekov <https://it-projects.info/team/fedoranvar>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models

from ..lib import pinguin

PREFIX = "__base_api__"


class Base(models.AbstractModel):

    _inherit = "base"

    @api.model
    def search_or_create(self, vals, active_test=True):
        domain = [
            (k, "=", v)
            for k, v in vals.items()
            if not self._fields.get(k).type.endswith("2many")
        ]
        records = self.with_context(active_test=active_test).search(domain)
        is_new = False
        if not records:
            is_new = True
            records = self.create(vals)
        return (is_new, records.ids)

    @api.model
    def search_read_nested(
        self, domain=None, fields=None, offset=0, limit=None, order=None, delimeter="/"
    ):
        result = pinguin.get_dictlist_from_model(
            self._name,
            tuple(fields),
            domain=domain,
            offset=offset,
            limit=limit,
            order=order,
            env=self.env,
            delimeter=delimeter,
        )
        return result

    @api.model
    def create_or_update_by_external_id(self, vals):
        ext_id = vals.get("id")
        is_new = False
        imd_env = self.env["ir.model.data"]
        # if external id not defined
        if not isinstance(ext_id, str):
            raise ValueError('"id" field must be type of "string"')
        # if x2x fields values are exist
        fields_2many = []

        def convert_external_2_inner_id(ext_id, field):
            try:
                result = imd_env._xmlid_lookup(PREFIX + "." + ext_id)[2]
            except ValueError as e:
                raise ValueError(
                    "No object with external id in field {}: {}".format(field, ext_id)
                ) from e
            return result

        for field in vals:
            # for many2one fields
            if self._fields[field].type == "many2one" and isinstance(vals[field], str):
                vals[field] = convert_external_2_inner_id(vals.get(field), field)
            elif self._fields[field].type.endswith("2many"):
                fields_2many.append(field)

        # for x2many fields
        for field in fields_2many:
            for index, tuple_record in enumerate(vals[field]):
                list_record = list(tuple_record)
                if list_record[0] in [1, 2, 3, 4] and isinstance(list_record[1], str):
                    list_record[1] = convert_external_2_inner_id(list_record[1], field)
                elif list_record[0] == 6:
                    for record_for_replace in list_record[2]:
                        if isinstance(record_for_replace, str):
                            record_for_replace = convert_external_2_inner_id(
                                record_for_replace, field
                            )
                vals[field][index] = tuple(list_record)

        # If external id exists...
        try:
            inner_id = imd_env._xmlid_lookup(PREFIX + "." + ext_id)[2]
        # No: Create record and register external_key
        except ValueError:
            is_new = True
            inner_id = self.create(vals).id
            imd_env.create(
                {
                    "name": vals.get("id"),
                    "model": self._name,
                    "module": PREFIX,
                    "res_id": inner_id,
                }
            )
        else:
            # Yes: Write changes to record
            self.browse(inner_id).write(vals)

        return (is_new, inner_id)
