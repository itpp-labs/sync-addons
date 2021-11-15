.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

========================
 Multichannel Live Chat
========================

Base module to implement Live Chat through different channels (Telegram, WhatsApp, Instragram, etc.).

Usage
=====

Add following code to your module:


.. code-block:: py

    from odoo import fields, models


    class MailChannel(models.Model):
        _inherit = "mail.channel"

        channel_type = fields.Selection(
            selection_add=[("multi_livechat_NAME", "Channel Description")],
        )


Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============

* `Ivan Yelizariev <https://twitter.com/yelizariev>`__
* `Eugene Molotov <https://github.com/em230418>`__

Further information
===================

Apps store: https://apps.odoo.com/apps/modules/13.0/multi_livechat/

Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/13.0/multi_livechat.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/13.0/multi_livechat.atom>`_

Tested on `Odoo 13.0 <https://github.com/odoo/odoo/commit/3097e0b977ddbaa9efc4c3e60399d169dee45604>`_
