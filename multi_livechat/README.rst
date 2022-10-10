.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

===============
 Customer Chat
===============

Base module to implement Live Chat through different channels (Telegram, WhatsApp, Instragram, etc.).

Usage
=====

Add following code to your module. Replace MODULE and NAME for your custom values, e.g.

* `MODULE` is `sync_telegram`
* `NAME` is `telegram`


MODULE/__manifest__.py
----------------------

.. code-block:: py

    "depends": ["multi_livechat"],
    "assets": {
        "web.assets_backend": [
            "MODULE/static/src/models/discuss/discuss.js",
            "MODULE/static/src/models/discuss_sidebar_category/discuss_sidebar_category.js",
        ],
    },


MODULE/models/__init__.py
----------------------

.. code-block:: py

    from . import res_users_settings
    from . import mail_channel


MODULE/models/res_users_settings.py
-----------------------------------

.. code-block:: py

    from odoo import fields, models

    
    class ResUsersSettings(models.Model):
        _inherit = 'res.users.settings'
    
        is_discuss_sidebar_category_NAME_open = fields.Boolean("Is category NAME open", default=True)


MODULE/models/mail_channel.py
-----------------------------

.. code-block:: py

    from odoo import fields, models


    class MailChannel(models.Model):
        _inherit = "mail.channel"

        channel_type = fields.Selection(
            selection_add=[("multi_livechat_NAME", "Channel Description")],
            ondelete={"multi_livechat_NAME": "cascade"}
        )

MODULE/static/src/models/discuss/discuss.js
-------------------------------------------

.. code-block:: js

    /** @odoo-module **/
    
    import { registerFieldPatchModel } from '@mail/model/model_core';
    import { one2one } from '@mail/model/model_field';
    
    registerFieldPatchModel('mail.discuss', 'MODULE/static/src/models/discuss/discuss.js', {
        categoryMLChat_NAME: one2one('mail.discuss_sidebar_category', {
            inverse: 'discussAsMLChat_NAME',
            isCausal: true,
        }),
    });


MODULE/static/src/models/discuss_sidebar_category/discuss_sidebar_category.js
-----------------------------------------------------------------------------

.. code-block:: js

    /** @odoo-module **/

    import { registerFieldPatchModel, registerIdentifyingFieldsPatch } from '@mail/model/model_core';
    import { one2one } from '@mail/model/model_field';

    registerFieldPatchModel('mail.discuss_sidebar_category', 'MODULE', {
        discussAsMLChat_NAME: one2one('mail.discuss', {
            inverse: 'categoryMLChat_NAME',
            readonly: true,
        }),
    });

    registerIdentifyingFieldsPatch('mail.discuss_sidebar_category', 'MODULE', identifyingFields => {
        identifyingFields[0].push('discussAsMLChat_NAME');
    });

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Further information
===================

Apps store: https://apps.odoo.com/apps/modules/15.0/multi_livechat/

Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/15.0/multi_livechat.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/15.0/multi_livechat.atom>`_

Tested on `Odoo 15.0 <https://github.com/odoo/odoo/commit/172359c4a72d4a02e74eb63c70f8776c1cae946b>`_
