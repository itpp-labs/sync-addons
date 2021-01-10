.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

=========================
 WooCommerce Integration
=========================

Integration with https://woocommerce.com/

Sandbox
=======

To install local WooCommerce add following specification to your docker-compose.yml::

    services:

      # ...

      woo_db:
        image: mysql:5.7
        volumes:
            - woo_db:/var/lib/mysql
        environment:
          MYSQL_ROOT_PASSWORD: pass
          MYSQL_DATABASE: woo
          MYSQL_USER: woo
          MYSQL_PASSWORD: woo

      woo:
        image: wordpress:latest
        depends_on:
          - woo_db
        ports:
          - 80:80
        environment:
          WORDPRESS_DB_HOST: woo_db:3306
          WORDPRESS_DB_USER: woo
          WORDPRESS_DB_PASSWORD: woo
        volumes:
          - woo:/var/www/html/wp-content

      woo_ssl:
        image: foxylion/nginx-self-signed-https
        environment:
          REMOTE_URL: http://woo:80

    volumes:
      woo:
      woo_db:

Note, port 80 must be not occupied. You cannot change this settings, because otherwise webhooks will not work.

Open http://localhost/wp-admin/ and follow setup instructions

Navigate to ``Plugins >> Add New >> search for "woocommerce"``,  click `[Install Now]` and then `[Activate]`.

Add some products.

In Odoo set:
* ``API_URL`` to ``https://woo_ssl``.
* ``API_VERIFY_SSL`` to ``0``

To setup webhooks from WooCommerce to Odoo:

* Odoo must be available under valid SSL ceritificate! See `Sync Studio's README <../sync/README.rst>`__ for instruction how to make in 
* set System Parameters:

  * ``web.base.url`` -> ``https://YOUR_ADDRESS``
  * ``web.base.url.freeze`` -> *any value*
* Check WooCommerce configuration section in `<doc/index.rst>`__
* run  ``SETUP_WOO_WEBHOOKS``
* finaly, open Woo and check `webhooks <https://docs.woocommerce.com/document/webhooks/>`__
* On running Odoo use ``--db-filter=^YOUR_DATABASE_NAME$`` or make sure you have one database only
* In wordpress, in menu ``Settings > General Settings`` check that ``WordPress Address (URL)`` and ``Site Address (URL)`` have address ``http://localhost:80``
* Be sure that cron in WordPress is working. You can install plugin https://wordpress.org/plugins/wp-crontrol/ to get more information about cron
* To get webhook logs in Wordpress: open menu ``WooCommerce >> Status >> Logs``, select log file and click `[View]`
* Remember what webhooks in Wordpress works via cron, so you many need to wait up to 1 minute before webhook is fired

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Further information
===================

Apps store: https://apps.odoo.com/apps/modules/12.0/sync_woo/

Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/12.0/sync_woo.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/12.0/sync_woo.atom>`_

Tested on `Odoo 12.0 <https://github.com/odoo/odoo/commit/84d554f436ab4c2e7fa05c3f4653244a50fcc495>`_
