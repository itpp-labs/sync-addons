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

* Send message ``/newbot`` to @BotFather and follow further instructions to create a bot and get the bot token

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

You can continue chatting this way

File sending and receiving
--------------------------
The operator has the ability to send not just text messages, but also messages with attachments.

The Telegram Bot API has a `limit <https://core.telegram.org/bots/api#inputfile>`__ on the files sent through the bot:
 - The operator cannot send to Telegram user more than **10 MB for photos** and **50 MB for other files**.
 - Also, the operator cannot receive **files larger than 20 MB** from a Telegram user.

Subscribing telegram user to chatter
------------------------------------
After the bot has created a record, you can also send messages to telegram user directly from the record page (Lead, Task, etc.).
In order to do that, subscribe corresponding channel to the record.
Use button ``Show Followers -> Add Channels``.
