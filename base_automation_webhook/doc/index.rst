===================
 Outgoing Webhooks
===================

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Automation >> Automated Actions``
* Create new record and set field **Action To Do** to *Execute Python Code*. 
  For example:

  * **Action Name**: *Test*
  * **Model**: *Contact*
  * **Trigger Condition**: *On Creation*
  * **Before Update Domain**: Optional. You can specify a condition that must be
    satisfied before record is updated. The field may not be available
    depending on **Trigger Condition** value.
  * **Action To Do**: *Execute Python Code*
  * **Apply on**: Optional. You can specify a condition that must be satisfied before executing the Python Code.
  * **Python Code**:
    ::
        WEBHOOK="https://PASTE-YOUR-WEBHOOK-URL"
        data = {
            "partner_id": record.id,
            "partner_name": record.name,
        }
        requests.post(WEBHOOK, data)

  * Save everything

Usage
=====

* Make corresponding action (in our example, create new Contact)
* RESULT: the event is notified via webhook


Handling field changing
=======================

If you need to call a webhook on updating specific field, do as following:

* set **Before Update Domain** to a domain like ``[['FIELD', '!=', TARGET_VALUE]]``
* set **Apply On** to a domain like  ``[['FIELD', '=', TARGET_VALUE]]``

RESULT: webhook will be sent only when field value is changed to *TARGET_VALUE*.
