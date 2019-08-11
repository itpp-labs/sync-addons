===================
 Outgoing Webhooks
===================

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

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
  * **Server actions to run**:

    * **Action Name**: *Test Action*
    * **Action To Do**: *Execute Python Code*
    * **Python Code**: ```
WEBHOOK="https://PASTE-YOUR-WEBHOOK-URL"
data = {
    "partner_id": record.id,
    "partner_name": record.name,
}
requests.post(WEBHOOK, data)
```

  * Save everything

Usage
=====

* Make corresponding action (in our example, create new Contact)
* RESULT: the event is notified via webhook
