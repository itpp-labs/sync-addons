=================================
 WhatsApp (Chat API) Integration
=================================

In order to work with this module, you need to have one of following instance:

* Chat API instance (you need to pay for subscription)
* Replica Chat API instance (free, selfhosted)

Chat API configuration
======================

* Register in Chat API: https://app.chat-api.com/
* Choose WhatsApp project
* Follow "Attention message". Choose authorization method depending on given message
* Scan QR code using WhatsApp
* Remember given "Your API URL" and "token"

Replica Chat API instance
=========================

Follow instructions from https://github.com/itpp-labs/whatsapp-api-service

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation

 Specific installation of queue_job
-----------------------------------

If messages from Odoo to WhatsApp Bot haven't been sent the problem may be in the wrong `queue_job` installation.
You should check how to install this module in its `docs <https://github.com/OCA/queue/tree/14.0/queue_job#installation>`__
In particular, you need to add `queue_job` to `server_wide_modules`.

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Choose ``WhatsApp (Chat API)`` project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:

  * ``WHATSAPP_CHATAPI_API_URL``
  * ``WHATSAPP_CHATAPI_TOKEN``

Usage
=====

WhatsApp:

* send some message to the created bot

In Odoo:

* Open ``[[ Discuss ]]`` menu
* RESULT: there is new channel for the whatsapp contact
* Open the channel and reply to message

In WhatsApp:

* RESULT: the message is delivered via bot

You can continue chatting this way
