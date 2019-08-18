==========================
 REST API/Openapi/Swagger
==========================

.. contents::
   :local:

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way
* Add ``openapi`` to ``--load`` parameters, e.g.::

    ./odoo --workers=2 --load openapi,web --config=/path/to/openerp-server.conf

Configuration
=============

Activating and customization
----------------------------

.. via Model's Menu (recommended)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. TODO
.. * `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
.. * Open the developer tools drop down
.. * Click menu ``Configure REST API`` located within the dropdown
.. * On the form that opens, activate and configure this module for REST API accessability. 
.. * Click ``[Apply]``
.. 
.. via Database Structure Menu (only for developers)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Open menu ``[[ OpenAPI ]] >> OpenAPI >> Integrations``
* Click ``[Create]``
* Specify **Name** for integration, e.g. ``test``
* Set **Log requests** to *Full*
* Set **Log responses** to *Full*
* In ``Accessable models`` tab click ``Add an item`` 
  * Set **Model**, for example *res.users*
  * Configure allowed operations

    * **[x] Create via API**

      * Set **Creation Context Presets**, for example

        * **Name**: ``brussels``
        * **Context**: ``{'default_tz':'Europe/Brussels', 'default_lang':'fr_BE'}``

    * **[x] Read via API**

      * Set **Read One Fields** -- fields to return on reading one record
      * Set **Read Many Fields** -- fields to return on reading multiple records

      Note: you can use Export widget in corresponding *Model* to create *Fields list*. To do that:

        * Open menu for the *Model*
        * Switch to list view
        * Select any record
        * click ``[Action] -> Export``
        * Set **Export Type** to *Export all Data*
        * Add the fields you need to right column
        * Click **Save fields list**, choose name and save the list
        * Now the list is availab to set **Read One Fields**, **Read Many Fields** settings

    * **[x] Update via API**
    * **[x] Delete via API**

Authentication
--------------

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Users >> Users``
* Select a user that will be used for iteracting over API
* In **Allowed Integration** select some integrations
* Copy **OpenAPI Token** to use in any system that support REST API (OpenAPI)


Configuration review
--------------------

All settings are available under menu ``[[ Settings ]] >> REST API`` (Available in `Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__)

Usage
=====

TODO

* Open menu ``[[ Settings ]] >> Dashboard``
* In *REST API* section you can see Quantity of Models available via API
* Click button ``[Manage]`` to check or edit configuration
* Click link ``Publish OpenAPI (Swagger)``. A ``swagger.json`` will be made available under ``/api/v1/swagger.json``
  documentation of the tool / system you use on how to apply the Specification
  file there. Some examples are presented below.

Swagger Editor
--------------

Allows to review API

* Open http://editor.swagger.io/
* Click menu ``File >> Import File`` 
* RESULT: You can see specification for API
* You can auto-generate SDKs in over 40 languages, there.
* Or even download server stups in over 20 frameworks, that iplement the API.
