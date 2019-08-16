.. image:: https://img.shields.io/badge/license-LGPL--3-blue.png
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

==========================
 REST API/Openapi/Swagger
==========================

Set up REST API and export Open API (Swagger) specification file for
integration with whatever you need.

This module implements a ``/api/v1/`` route tree.

Authentication
==============

* Server wide "break glass" through a ``salt`` in the config file
* Database inference: Database name encoded and appended to the token
* User authentication through the actual token

As a workaround for multi-db instances, system uses *Basic Authentication* with
``db_name:token`` credentials, where ``token`` is a new field in ``res.users``
model.

Customization
=============

TODO

The module already includes configuration for the following models:

  * report
  * sale.order
  * sale.order.line
  * account.invoice
  * account.invoice.line
  * res.partner
  * product.template

TODO: Redefine `ir.model` to load default configuration on load

The module allows to configure

* available models
* available operations per model (CRUD)
* enable/disable private methods through API
* method whitelist
* specification for the following operations

  * For reading ONE:

    * return field sets

  * For reading MULTI:

    * return field sets

.. TODO: add example of usage in API requests

  * For creation:

    * Create context (default values & context flags)

.. TODO: add example of usage in API requests


Check `Usage instruction <doc/index.rst>`_ for details.

Roadmap
=======

* TODO: monkey patch doesn't work just after odoo restart. Either update docs to ask add the module to server_wide_modules or find a workaround
* TODO: Add a smart button for Logs in ``openapi.namespace`` form

Credits
=======

Contributors
------------
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__
* `David Arnold <dar@xoe.solutions>`__

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__
* `XOE Solutions <https://xoe.solutions>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

      To get a guaranteed support you are kindly requested to purchase the module at `odoo apps store <https://apps.odoo.com/apps/modules/10.0/openapi/>`__.

      Thank you for understanding!

      `IT-Projects Team <https://www.it-projects.info/team>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/misc-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/openapi/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Notifications on updates: `via Atom <https://github.com/it-projects-llc/misc-addons/commits/10.0/openapi.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/it-projects-llc/misc-addons/commits/10.0/openapi.atom>`_

Tested on Odoo 10.0 87b42ad9a887faacbbefcab9dd0703a5c51ce28b
