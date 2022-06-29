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
            ondelete={"multi_livechat_NAME": "cascade"}
        )


Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Further information
===================

Apps store: https://apps.odoo.com/apps/modules/14.0/multi_livechat/

Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/14.0/multi_livechat.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/14.0/multi_livechat.atom>`_

Tested on `Odoo 14.0 <https://github.com/odoo/odoo/commit/3780fa2af5d5f6cac91e419bcab69a253db280bd>`_
