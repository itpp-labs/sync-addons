This document describes Sync Studio tools that help implementing basic syncronization between systems (internal and external).


For one2one syncronization you can use following helpers.

* ``MAGIC.sync_odoo2x(src_list, sync_info, create=False, update=False)``

  * ``sync_info["x"]["create"](odoo_record) -> external_ref``: create external record and return reference
  * ``sync_info["x"]["update"](external_ref, odoo_record) -> external_ref``: update external record
  * ``sync_info["x"]["get_ref"](x)``: get reference for an item in src_list

* ``MAGIC.sync_x2odoo(src_list, sync_info, create=False, update=False)``

  * ``sync_info["odoo"]["create"](x) -> odoo_record``: create odoo record from external data
  * ``sync_info["odoo"]["update"](odoo_record, x) -> odoo_record``:  update odoo record according to providing external data

Common args:

* ``sync_info["relation"]``: same as ``relation_name`` in ``set_link``, ``get_link``
* ``src_list``: iterator of ``x`` or ``odoo_record`` values
*  ``create``: boolean value for "create record if it doesn't exist"
*  ``update``: boolean value for "update record if it exists"

To use helpers, create ``sync_info`` with all information, e.g.

.. code-block:: python

     EMPLOYEE_SYNC = {
       "relation": "my_system_and_odoo_employee_rel",
       "x": {
         "get_ref": employee2ref,
         "create": employee_create,
         "update": employee_update,
       },
       "odoo": {
         "create": employee_create_odoo,
         "update": employee_update_odoo,
       }
     }

Then you can reuse in all syncronizations, e.g.

.. code-block:: python

    # on initial fetching records from external system
    sync_x2odoo(all_employees_x, EMPLOYEE_SYNC, create=True)

    # to push all updates to external system
    sync_odoo2x(all_employees_odoo, EMPLOYEE_SYNC, update=True)

    # on updating a single record push all updates to external system
    sync_odoo2x([employee_odoo], EMPLOYEE_SYNC, update=True)


There is a similar helper for syncronization between two external systems:

* ``MAGIC.sync_external(src_list, relation, src_info, dst_info, create=False, update=False)``

  * ``src_info["get_ref"](src_data)``: get reference for an item in src_list
  * ``src_info["system"]``: e.g. ``"github"``
  * ``src_info["update"](dst_ref, src_data)``
  * ``src_info["create"](src_data) -> dst_ref``
  * ``dst["system"]``: e.g. ``"trello"``
