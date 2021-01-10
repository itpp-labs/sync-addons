=========================
 WooCommerce Integration
=========================

WooCommerce configuration
=========================

Configure REST API Secret/Key pair in according to `WooCommerce Documentation <https://docs.woocommerce.com/document/woocommerce-rest-api/>`__.

Activate *Pretty permalinks* in Settings > Permalinks so that the custom endpoints are supported. Default permalinks will not work. For example, in WordPress v5.6, you can select *Post name* option.

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/12.0/sync/>`__ Documentation
* Install python packages:

    python3 -m pip install woocommerce

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Choose ``WooCommerce`` project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:

  * ``API_URL``
  * ``API_KEY``
  * ``API_SECRET``

* Click ``[Run Now]`` button in ``SETUP_WOO_WEBHOOKS``
* For initial synchronization click ``[Run Now]`` on corresponding Manual Triggers that get records from one system and create on another. E.g. to sync products there are 2 available buttons:

  * CREATE_PRODUCTS_WOO2ODOO
  * CREATE_PRODUCTS_ODOO2WOO

* Open a task *Sync Odoo to WooCommerce*, configure and activate DB Triggers
* If you for any reason you cannot use instant syncronization (i.e. via DB Triggers and Webhooks), you can schedule periodic syncronization by activating Cron trigers in corresponding tasks

Usage
=====

Make updates in one system and click corresponding ``UPDATE_...`` button in
Manual Triggers. Note, that update buttons works only with previously linked
records (i.e. ones synced via ``CREATE_...`` button). RESULT: records are
synced.
