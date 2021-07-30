=======================
 Odoo2odoo Integration
=======================

In this project we push partners to external Odoo and sync back changes.

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation


Configuration
-------------

* Install ``Contacts`` module and create sevreal contacts just for test
* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Odoo2odoo integration* project
* Go to ``Parameters`` tab
* Click ``[Edit]``
* Set **Parameters** and **Secrets**:
  * URL, e.g. ``https://3674665-12-0.runbot41.odoo.com``
  * DB, e.g. ``3674665-12-0``
  * USERNAME, e.g. ``admin``
  * PASSWORD, e.g. ``admin``

Usage
=====

In this example we run local server, that synchronize data with main server to solve connection issues

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Odoo2odoo integration* project
* Unarchive the project
* Click ``Available Tasks`` tab
* Click ``[Edit]``
* Go to ``Sync Remote Models Updates`` task
* Click on ``Available Triggers`` tab and go inside ``CHECK_EXTERNAL_ODOO`` trigger
* Configure cron
* Make trigger Active on the upper right corner
* Click ``[Save]``

* Then you can trigger synchronization in some of the following ways:

  1. Click ``[Run Manually]`` inside the trigger

  2. Simply wait up to cron job will start on a schedule :)


**Uploading all existing partners.**

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Demo Odoo2odoo Integration* project
* Choose Sync Task *Sync Local Models To Remote Odoo*
* Click button ``[Run Now]``
* Open the external Odoo
* Make sure contacts created or changed in the external Odoo

  * RESULT: copies of all our partners are in the external Odoo; they have a comment *by Sync Studio:* in Internal Notes of a partner







старый сценарий использования

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Odoo2odoo integration* project
* Unarchive the project
* Go to ``Manual Triggers`` tab
* Click ``[Run Now]`` button in ``PUSH_LOCAL_DATA``
* Make sure contacts appear in  the external Odoo
* Change name or avatar of the external contact
* Get back to Sync Studio
* Click ``[Run Now]`` button in ``PULL_EXTERNAL_DATA``
* Make sure this contact changed in the local Odoo
