===================
 Viber Integration
===================

Viber configuration
===================

`Create Viber bot <https://partners.viber.com/account/create-bot-account>`__ and get Token of the bot.

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation
* Install python packages::

    python3 -m pip install viberbot

* Due to `Odoo limitations <https://github.com/odoo/odoo/issues/57133>`__, one of the following workarounds should be applied on setting up webhooks:

    * either delete `line <https://github.com/odoo/odoo/blob/db25a9d02c2fd836e05632ef1e27b73cfdd863e3/odoo/http.py#L326>`__ that raise exception in case of type mismatching (search for ``Function declared as capable of handling request of type`` in standard Odoo code). In most cases, this workaround doesn't need to be reverted
    * or open file ``sync/controllers/webhook.py`` and temporarily change ``type="json"`` to ``type="http"``

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Choose ``Viber`` project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:

  * ``VIBER_BOT_TOKEN``
  * ``BOT_NAME``
  * ``BOT_AVATAR_URL``

* Click ``[Run Now]`` button in ``SETUP_WEBHOOK``

Usage
=====

Viber:

* send some message to the created bot

In Odoo:

* Open ``[[ Discuss ]]`` menu
* RESULT: there is new channel for the viber contact
* Open the channel and reply to message

In telegram:

* RESULT: the message is delivered via bot

You can continue chatting this way
