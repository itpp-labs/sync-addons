.. image:: https://img.shields.io/badge/license-LGPL--3-blue.png
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

==========================
 REST API/OpenAPI/Swagger
==========================

Set up REST API and export OpenAPI (Swagger) specification file for integration
with whatever system you need. All can be configured in Odoo UI, no extra module
is needed.

This module implements a ``/api/v1/`` route tree.

Authentication
==============

* Database inference: Database name encoded and appended to the token
* User authentication through the actual token

As a workaround for multi-db Odoo instances, system uses *Basic Authentication* with
``db_name:token`` credentials, where ``token`` is a new field in ``res.users``
model. That is, whenever you see Username / Password to setup OpenAPI
connection, use Database Name / OpenAPI toekn accordingly.

Roadmap
=======

* TODO: Add a smart button for Logs in ``openapi.namespace`` form
* TODO: Add a button to developer menu to grant access to current model

    * `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
    * Open the developer tools drop down
    * Click menu ``Configure REST API`` located within the dropdown
    * On the form that opens, activate and configure this module for REST API accessability. 
    * Click ``[Apply]``




Credits
=======

Contributors
------------
* `David Arnold <dar@xoe.solutions>`__
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__
* `Rafis Bikbov <https://it-projects.info/team/RafiZz>`__
* `Stanislav Krotov <https://it-projects.info/team/ufaks>`__

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

Demo: http://runbot.it-projects.info/demo/sync-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/openapi/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Notifications on updates: `via Atom <https://github.com/it-projects-llc/sync-addons/commits/10.0/openapi.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/it-projects-llc/sync-addons/commits/10.0/openapi.atom>`_

Tested on Odoo 10.0 87b42ad9a887faacbbefcab9dd0703a5c51ce28b
