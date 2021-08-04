.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

=============
 Sync Studio
=============

Synchronize anything with anything:

* System X ↔ Odoo
* Odoo 1 ↔ Odoo 2
* System X ↔ System Y

Provides a single place to handle synchronization trigered by one of the following events:

* **Cron** -- provided by ``ir.cron``
* **DB Event** -- provided by ``base.automation``
* **Incoming webhook** -- modified version of ``/website/action`` controller from ``website`` module
* **Manual Triggering** -- provided by ``ir.actions.server``. User needs to click a button to run this action

Difference with built-in code evaluation:

* Allows to use json format for incomming webhooks
* Provides helpers for resource linking. See *Links* section in `<doc/index.rst>`__
* Uses queue_job module as a job broker
* Asynchronous calls to split big task into few small ones
* Allows repeat job on temporary fails (e.g. when external API is not available)

Roadmap
=======

* Code widget: show line numbers
* Webhooks: add a possibility to retry failed webhook (e.g. to debug code)
* Webhooks: during the migration rename `website` appearances in links to `sync`. We decided not to do this in the stable branch to not break existing integrations

Developer Hints
===============

Public webhook address
----------------------

If you run Odoo locally and need to test webhook, your Odoo server should be available via public URL. You can either use specialized services like https://ngrok.com/ or make proxing via ssh tunneling as described in the next section. Once it's done set corresponding ``https://...`` value for ``web.base.url`` parameter (menu ``[[ Settings ]] >> System Parameters``). Also, you should set any value to  `web.base.url.freeze <https://odoo-source.com/?q=web.base.url.freeze&i=nope&files=&excludeFiles=po%24%7Cpot%24%7Cyml%24%7Cyaml%24%7Ccss%24%7C%2Fstatic%2Flib%2F&repos=odoo>`__ to avoid automatic change of ``web.base.url``.

SSH tunneling
~~~~~~~~~~~~~

* Connect your server:

  * Edit file ``/etc/ssh/sshd_config``:

    * Find ``GatewayPorts`` attribute and set value to ``yes``

  * Restart ssh daemon::

        service ssh restart

* Connect to your server with ``-R`` attribute::

      ssh user@yourserver.example -R 0.0.0.0:8069:localhost:8069

Now you can use ``http://yourserver.example:8069`` as a value for ``web.base.url`` in Odoo.

Few more steps requires to use https connection (e.g. telegram api works with https only). In your server do as following:

* Install nginx in your server
* Add nginx config::

      server {
             listen 80;
             server_name yourserver.example;
             location / {
                  proxy_set_header Host $host;
                  proxy_pass http://localhost:8069;
             }
      }

* Install `certbot <https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx.html>`__
* Run
  ::

     sudo certbot --nginx

* Done!

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* `Ivan Yelizariev <https://twitter.com/yelizariev>`__:

      * :one::two: init version of the module
      * :one::two: redesign module to prevent odoo container escapes

Further information
===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/14.0/sync/


Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/14.0/sync.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/14.0/sync.atom>`_

Tested on `Odoo 14.0 <https://github.com/odoo/odoo/commit/6916981f56783de7008cd04d4e37e80166150ff7>`_
