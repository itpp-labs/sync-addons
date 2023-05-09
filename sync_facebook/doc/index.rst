======================
 Facebook Integration
======================

Facebook configuration
======================

Facebook App
------------

* `Create new Facebook App <https://developers.facebook.com/apps>`__

  * **App type:** Business
  * **Apps Purpose:** Yourself or your own business

* In Facebook App page open ``Settings >> Basic`` to get **App ID** and **App Secret**

Facebook Page
-------------

* `Select your page <https://www.facebook.com/pages/>`__ or `create new one <https://www.facebook.com/pages/creation>`__
* Get **Page ID** from Page url. For example, for Page ``https://www.facebook.com/Facebook-intergration-testing-123456789`` Page ID is 123456789

Facebook Page: Lead Ad
----------------------

* `Create a Lead Ad <https://www.facebook.com/business/help/397336587121938>`__ via menu ``Publishing Tools >> Forms Library``
* Once form is created, click `[Create Ad]` button

Facebook Page: Access Token
---------------------------

* Open `Graph API Explorer <https://developers.facebook.com/tools/explorer/>`__
* Select Facebook App
* Select option "User Access Token"
* Select required `permisions <https://developers.facebook.com/docs/pages/overview/permissions-features>`__, e.g.:

  * public_profile
  * pages_show_list
  * pages_read_engagement
  * leads_retrieval
  * pages_manage_metadata

You can ignore warning "Submit for Login Review". It just means that you cannot
work with Facebook Pages where you don't have a role.

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/12.0/sync/>`__ Documentation
* Install python packages:

    python3 -m pip install facebook_business

* Due to `Odoo limitations <https://github.com/odoo/odoo/issues/57133>`__, one of the following workarounds should be applied on setting up webhooks:

    * delete `line <https://github.com/odoo/odoo/blob/db25a9d02c2fd836e05632ef1e27b73cfdd863e3/odoo/http.py#L326>`__ that raise exception in case of type mismatching (search for ``Function declared as capable of handling request of type`` in standard Odoo code). In most cases, this workaround doesn't need to be reverted
    * open file ``sync/controllers/webhook.py`` and temporarily change ``type="json"`` to ``type="http"``

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Choose ``Facebook`` project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:

  * ``APP_ID``
  * ``APP_SECRET``
  * ``PAGE_ID``
  * ``USER_ACCESS_TOKEN``

* Click ``[Run Now]`` button in ``GENERATE_PAGE_ACCESS_TOKEN``
* Click ``[Run Now]`` button in ``SETUP_APP``
* Click ``[Run Now]`` button in ``SETUP_PAGE_WEBHOOK``

Usage
=====

Lead Ads
--------

Create a lead in facebook and check that it's synced to Odoo
