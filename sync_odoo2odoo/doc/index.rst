=======================
 Odoo2odoo Integration
=======================

This module adds new *Evaluation Context* with helpers for odoo2odoo
integration:

* `record2dict(record, fields)`
* `odoo_execute_kw(model, method, *args, **kwargs)`
* `sync_odoo2odoo_push(model_name, domain=None, fields=None, active_test=True, create=False, update=False, records=None)`
* `sync_odoo2odoo_pull(model_name, domain=None, fields=None, active_test=True, create=False, update=False)`

The module is packaged with a draft Sync Project that implements one2one syncronization of listed models and specified fields. By default it syncs Partner and Product records that contains `test` in their names.

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/15.0/sync/>`__ Documentation


Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Odoo2odoo integration* project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets** for remote database:
  * URL, e.g. ``https://3674665-12-0.runbot41.odoo.com``
  * DB, e.g. ``3674665-12-0``
  * USERNAME, e.g. ``admin``
  * PASSWORD, e.g. ``admin``

Usage
=====

On remote database:

* Create some partners with word *test* in the name field
* Create some products with word *test* in the name field

On local database (the one with Sync Studio installed)

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Odoo2odoo integration* project
* Unarchive the project
* Click ``Available Tasks`` tab
* Click ``[Edit]``
* Go to ``Sync Remote Models Updates`` task
* Click on ``Available Triggers`` tab and go inside ``CHECK_EXTERNAL_ODOO`` trigger
* Configure cron
* Make trigger Active on the upper right corner
* Click ``[Save]``

* Then you can trigger synchronization in one of the following ways:

  1. Click ``[Run Manually]`` inside the trigger

  2. Simply wait up to cron job will start on a schedule :)

RESULT: contacts and products are synced to local database

Local to remote syncronization works in the same way, but with additional feature: on creating a new local record, it's pushed to remote server immediately (depending on DB triggers configuration)
