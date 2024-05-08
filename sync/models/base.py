# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import models


class Base(models.AbstractModel):
    _inherit = "base"

    def set_link(self, relation_name, ref, sync_date=None, allow_many2many=False):
        return self.env["sync.link"]._set_link_odoo(
            self, relation_name, ref, sync_date, allow_many2many
        )

    def search_links(self, relation_name, refs=None):
        return (
            self.env["sync.link"]
            .with_context(sync_link_odoo_model=self._name)
            ._search_links_odoo(self, relation_name, refs)
        )

    def _create_or_update_by_xmlid(self, vals, code, namespace="XXX", module="sync"):
        """
        Create or update a record by a dynamically generated XML ID.
        Warning! The field `noupdate` is ignored, i.e. existing records are always updated.

        Args:
            vals (dict): Field values for creating or updating the record.
            code (str): A unique part of the XML ID, usually a meaningful name or code.
            namespace (str, optional): Additional unique part of the XML ID.
            module (str, optional): The module name, defaults to 'sync'.

        Returns:
            odoo.models.BaseModel: The record that was created or updated.
        """
        # Construct the XML ID
        xmlid_code = f"MAGIC__{namespace}__{self._table}__{code}"
        xmlid_full = f"{module}.{xmlid_code}"

        # Try to retrieve the record using the XML ID
        data_obj = self.env["ir.model.data"]

        res_id = data_obj._xmlid_to_res_id(xmlid_full, raise_if_not_found=False)

        if res_id:
            # If record exists, update it
            record = self.browse(res_id)
            record.write(vals)
        else:
            # No record found, create a new one
            record = self.create(vals)
            # Also create the corresponding ir.model.data record
            data_obj.create(
                {
                    "name": xmlid_code,
                    "module": module,
                    "model": self._name,
                    "res_id": record.id,
                    "noupdate": False,
                }
            )

        return record
