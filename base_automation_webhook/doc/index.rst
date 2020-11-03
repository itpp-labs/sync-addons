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
* Create new record and attach an action to **Server actions to run** field.
  The action must have field **Action To Do** set to *Execute Python Code*.
  For example:

  * **Name**: *Test*
  * **Model**: *Contact*
  * **Trigger Condition**: *On Creation*
  * **Filter**: Optional. You can specify a condition that must be satisfied before executing the Rule.
  * **Server actions to run**:

    * **Action Name**: *Test Action*
    * **Action To Do**: *Execute Python Code*
    * **Condition**: Optional. You can specify a condition that must be satisfied before executing the Action.
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

* set Rule's **Filter** to a domain like ``FIELD is not equal to TARGET_VALUE``
* set Action's **Condition** to a domain like ``FIELD is equal to TARGET_VALUE``
