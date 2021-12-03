=========
 Mailgun
=========

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

Mailgun-side
------------

* register or log in http://mailgun.com
* Open menu ``[[ Domains ]]`` and click on your domain, e.g. ``sandbox123*****.mailgun.org`` domain. Here you can see all the information needed to configure odoo outgoing mail feature
* Please note that state of your domain should be ``Active`` before you can use it. If it is ``Unverified``, verify it first using Mailgun FAQ - `How do I verify my domain <https://help.mailgun.com/hc/en-us/articles/202052074-How-do-I-verify-my-domain->`__
* if you are using your sandbox domain, add Authorized Recipient first (Sandbox domains are restricted to `authorized recipients <https://help.mailgun.com/hc/en-us/articles/217531258>`__ only)
* create new Route

  * Open menu ``[[ Routes ]]``
  * Click ``[Create Route]`` button

    * **Expression Type** - ``Custom``
    * **Raw Expression** - ``match_recipient('.*@<your mail domain>')``
    * **Actions** - ``Store and notify``, ``http://<your odoo domain>/mailgun/notify``

Odoo-side
---------

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Configure **Outgoung mail server**

  * Open menu ``[[ Settings ]] >> Technical >> Email >> Outgoing Mail Servers``
  * Edit ``localhost`` record or create new one with the following:

    * **Description** - ``Mailgun``
    * **SMTP Server** - take from Mailgun **SMTP Hostname** (usually, it is ``smtp.mailgun.org``)
    * **Connection Security** - ``SSL/TLS``
    * **Username** - take from Mailgun **Default SMTP Login**
    * **Password** - take from Mailgun **Default Password**
    * Click ``[Test Connection]`` button to check the connection and then ``[Save]``

* Configure **Incoming mail feature**

  * Configure catchall domain

    * Open menu ``Settings / General Settings``, check **External Email Servers** and edit **Alias Domain** - set it from Mailgun **Domain Name**
    * Click ``[Save]`` button

  * Set Mailgun API credentials

    * Open menu ``[[ Settings ]] >> Parameters >> System Parameters``
    * Create new parameter

      * key: ``mailgun.apikey``
      * Value: API Key from mailgun (``key-...``)
      * Click ``[Save]`` button

  * Configure mail aliases and emails for users

    * Open menu ``[[ Settings ]] >> Users >> Users``
    * Select the ``Administrator`` user (for example, you should configure all your users the same way but using different aliases) and click ``[Edit]``
    * On Preference tab edit **Alias** field - create new mail alias, e.g. ``admin@<you mail domain>`` with the following settings

      * **Alias Name** - ``admin``
      * **Aliased Model** - ``Users``
      * **Record Thread ID** - ``1``
      * **Default Values** - ``{}``
      * **Alias Contact** - ``Everyone``
      * **Security Owner** - ``Administrator``
      * **Parent Model** - Not set
      * **Parent Record Thread ID** - ``0``

    * Open user's **Related Partner** and edit **Email** field - usually it should be the same as mail alias name (``admin@<you mailgun domain`` for ``Administrator``) - this would be an address for replying user's messages

Usage
=====

Outgoing
--------

* Open menu ``[[ Settings ]]>> Email >> Emails`` to create a message
* Click ``[Send Now]`` button
* RESULT: receive the message in your mail client (e.g. on gmail.com)

Incoming
--------

* Create new message from your mail client to e.g. ``admin@<you mailgun domain>``
* Open menu ``[[ Discuss ]]`` in Odoo
* RESULT: See your message there
