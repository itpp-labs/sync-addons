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

* Click ``[Save]``
* Copy **Specification Link** to use it in any system that support OpenAPI

Authentication
--------------

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Users >> Users``
* Select a user that will be used for iteracting over API
* In **Allowed Integration** select some integrations
* Copy **OpenAPI Token** to use it in any system that support OpenAPI

Usage
=====

As the simplest example, you can try API in Swagger Editor. It allows to review and check API

* Open http://editor.swagger.io/
* Click menu ``File >> Import File`` 
* Set **Specification link**
* RESULT: Specification is parsed succefully and you can see API presentation
* Click ``[Authorize]`` button

  * **Username** -- set database name
  * **Password** -- set **OpenAPI Token**

For more examples visit https://odoo-sync.sh website
