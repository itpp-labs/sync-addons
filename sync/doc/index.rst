=============
 Sync Studio
=============

.. contents::
   :local:

Installation
============

* Make configuration required for `queue_job <https://github.com/OCA/queue/tree/14.0/queue_job#id4>`__ module. In particular:

  * add ``queue_job`` to `server wide modules <https://odoo-development.readthedocs.io/en/latest/admin/server_wide_modules.html>`__, e.g.::

        --load base,web,queue_job

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way
* Install python package that you need to use. For example, to try demo projects install following packages:

    python3 -m pip install pyTelegramBotAPI PyGithub py-trello

* If your Sync projects use webhooks (most likely), be sure that url opens correct database without asking to select one

Odoo.sh
-------

`queue_job` may not work properly in odoo.sh with workers more than 1 due to `restrictions <https://github.com/OCA/queue/pull/256#issuecomment-895111832>`__  from Odoo.sh

For the `queue_job` work correctly in odoo.sh additional configuration is needed.

Add following lines to `~/.config/odoo.conf` and restart odoo via `odoo-restart` command in Webshell::

    [queue_job]
    scheme=https
    port=443
    host=ODOO_SH_ADDRESS.com


User Access Levels
==================

* ``Sync Studio: User``: read-only access
* ``Sync Studio: Developer``: restricted write access
* ``Sync Studio: Administrator``: same as Developer, but with access to the **Secrets** and to the Core Code

Running Job
===========

Depending on Trigger, a job may:

* be added to a queue or runs immediatly
* be retried in case of failure

  * if ``RetryableJobError`` is raised, then job is retried automatically in following scheme:

    * After first failure wait 5 minute
    * If it's not succeeded again, then wait another 15 minutes
    * If it's not succeeded again, then wait another 60 minutes
    * If it's not succeeded again, then wait another 3 hours
    * Try again for the fifth time and stop retrying if it's still failing

Cron
----

* job is added to the queue before run
* failed job can be retried if failed

DB
--

* job is added to the queue before run
* failed job can be retried if failed

Webhook
-------

* runs immediately
* failed job cannot be retried via backend UI; the webhook should be called again.

Button
------

* runs immediately
* to retry click the button again

Execution Logs
==============

In Project, Task and Job Trigger forms you can find ``Logs`` button in top-right
hand corner. You can filter and group logs by following fields:

* Sync Project
* Sync Task
* Job Trigger
* Job Start Time
* Log Level
* Status (Success / Fail)
