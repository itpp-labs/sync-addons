=====================
 Shopify Integration
=====================

Shopify configuration
=====================

* Log in to your store as the store owner.
* From your Shopify admin, go to Apps.
* Click Manage private apps.
* Click Enable private apps.
* Read and check the terms, and then click Enable private app development.
* Click "Create private app"
* Activate access to products ("read and write")
* "API Key" will be ``API_KEY`` and "Password" will be ``API_SECRET``

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Choose ``Shopify`` project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:

  * ``API_VERSION``
  * ``SHOP_DOMAIN``
  * ``API_KEY``
  * ``API_SECRET``

* Click ``[Run Now]`` button in ``SETUP_SHOPIFY_WEBHOOKS``
* For initial synchronization click ``[Run Now]`` on corresponding Manual Triggers that get records from one system and create on another. E.g. to sync products there are 2 available buttons:

  * CREATE_PRODUCTS_SHOPIFY2ODOO
  * CREATE_PRODUCTS_ODOO2SHOPIFY

* Open a task *Sync Odoo to Shopify*, configure and activate DB Triggers
* If for any reason you cannot use instant synchronization (i.e. via DB Triggers and Webhooks), you can schedule periodic syncronization by activating Cron trigers in corresponding tasks

Usage
=====

Make updates in one system and click corresponding ``UPDATE_...`` button in
Manual Triggers. Note, that update buttons works only with previously linked
records (i.e. ones synced via ``CREATE_...`` button). RESULT: records are
synced.
