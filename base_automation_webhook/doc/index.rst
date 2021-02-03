===================
 Outgoing Webhooks
===================

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Documentation
=============

``make_request`` is a wrapper for ``requests.request``. Check `requests lib documentation <https://requests.readthedocs.io/en/latest/api/#requests.request>`__ for details.

Configuration
=============

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Automation >> Automated Actions``
* Create new record and set field **Action To Do** to *Execute Python Code*.
  For example:

  * **Action Name**: *Test*
  * **Model**: *Contact*
  * **Trigger**: *On Creation*
  * **Apply on**: Optional. You can specify a condition that must be
    satisfied before record is updated. The field may not be available
    depending on **Trigger Condition** value.

  * **Action To Do**: *Execute Python Code*
  * **Python Code**:
    ::

        WEBHOOK="https://PASTE-YOUR-WEBHOOK-URL"
        data = {
            "partner_id": record.id,
            "partner_name": record.name,
        }
        make_request("POST", WEBHOOK, data=data)

  * Save everything

Testing
=======

* Make corresponding action (in our example, create new Contact)
* RESULT: the event is notified via webhook


Handling field changing
=======================

If you need to call a webhook on updating specific field, do as following:

* set **Apply On** to a domain like  ``[['FIELD', '=', TARGET_VALUE]]``

RESULT: webhook will be sent only when field value is changed to *TARGET_VALUE*.
