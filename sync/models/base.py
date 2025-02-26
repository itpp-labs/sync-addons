# Copyright 2020,2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import _, exceptions, models


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

    def _create_or_update_by_xmlid(self, vals, code, namespace="XXX", module="__sync"):
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
        record = None
        if res_id:
            record = self.browse(res_id)

        if record and record.exists():
            record.write(vals)
        else:
            # No record found, create a new one
            record = self.create(vals)
            if res_id:
                # exceptional case when data record exists, but record is deleted
                data_obj.search(
                    [("module", "=", module), ("name", "=", xmlid_code)]
                ).unlink()

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

    def _sync_field_name(self, property_name, property_type):
        sync_project_id = self.env.context.get("sync_project_id")

        if not sync_project_id:
            raise exceptions.UserError(
                _("The 'sync_project_id' must be provided in the context.")
            )

        return "x_sync_%s_%s_%s" % (sync_project_id, property_name, property_type)

    def _set_sync_value(self, property_name, property_type, property_value):
        """
        Set or create a property for the current record. If the field
        does not exist, create it dynamically.

        Args:
            property_name (str): Name of the property field to set.
            property_type (str): Type of the property field.
            property_value (Any): The value to assign to the property.
        """
        self.ensure_one()
        field_name = self._sync_field_name(property_name, property_type)
        field = self.env["ir.model.fields"].search(
            [
                ("name", "=", field_name),
                ("model", "=", self._name),
                ("ttype", "=", property_type),
            ],
            limit=1,
        )

        if not field:
            # Dynamically create the field if it does not exist
            field = self.env["ir.model.fields"].create(
                {
                    "name": field_name,
                    "ttype": property_type,
                    "model_id": self.env["ir.model"]._get_id(self._name),
                    "field_description": property_name.capitalize().replace("_", " "),
                }
            )
        self[field_name] = property_value

    def _get_sync_value(self, property_name, property_type):
        """
        Get the value of a dynamic field for the current record.

        Args:
            property_name (str): Name of the property field to get.
            property_type (str): Type of the property field.
        """
        self.ensure_one()
        field_name = self._sync_field_name(property_name, property_type)
        try:
            return self[field_name]
        except KeyError:
            return None
