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
* Get **Page ID** from the Page, that you want to connect to your chat bot. In order to do that, go to link ``https://www.facebook.com/your_page/about/``, where your_page is real url of your page. Then scroll to the bottom until you see "page ID" string. Copy the ID number given in **More info** section. Page ID is something like 123456789. Use it as your ``PAGE_ID`` parameter.


Facebook Page: Lead Ad
----------------------

* If you want to get leads from Facebook, you should create lead ad. To create that, do the following:
* `Create a Lead Ad <https://www.facebook.com/business/help/397336587121938>`__ via menu ``Publishing Tools >> Forms Library``
* Once form is created, click `[Create Ad]` button

Facebook Page: Access Token
---------------------------

* Open `Graph API Explorer <https://developers.facebook.com/tools/explorer/>`__
* Select Facebook App you created on a previous step in Facebook app Setting: <https://prnt.sc/1xa186e>
* Select option "Get User Access Token"
* Select required `permisions <https://developers.facebook.com/docs/pages/overview/permissions-features>`__, e.g.:

  * public_profile
  * pages_show_list
  * pages_read_engagement
  * leads_retrieval
  * pages_manage_metadata
  
* The result should look like that: <https://prnt.sc/1xa1kd3>
* Press the button `[generate Access token]`
* Save the resulted value from the field "Access Token" on the top". This would be your ``USER_ACCESS_TOKEN`

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
* Set **Parameters** and **Secrets**. You should edit the **Value** feilds. Fill them with data, received above:

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
