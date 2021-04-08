======================
 Telegram Integration
======================

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation


Configuration
=============

In Telegram
-----------

* Send message ``/new`` to @BotFather and follow further instructions to create a bot and get the bot token

In Odoo
-------

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Parameters >> System Parameters``
* Check that parameter ``web.base.url`` is properly set and it's accessible over
  internet (it should not localhost). Also, telegram accepts https addresses only (i.e. not http)
* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Telegram Integration* project
* Go to ``Parameters`` tab
* Set **Secrets**:

  * TELEGRAM_BOT_TOKEN

* Unarchive the project
* Open *Manual Triggers* Tab
* Click button ``[Run Now]`` near to *Setup* task

Usage
=====

In Telegram:

* send some message to the created bot

In Odoo:

* Open ``[[ Discuss ]]`` menu
* RESULT: there is channel with name *Telegram:<TELEGRAM NAME>* (the prefix can be configured in project parameter PARTNER_NAME_PREFIX)
* Open the channel and reply to message

In telegram:

* RESULT: the message is delivered via bot

You can continue chatting in this way
