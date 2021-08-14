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

    python3 -m pip install python-telegram-bot PyGithub py-trello

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
* ``Sync Studio: Administrator``: same as Developer, but with access to **Secrets**

Project
=======

* Open menu ``[[ Sync Studio ]] >> Projects``
* Create a project

  * **Name**, e.g. *Legacy migration*

  * In the ``Parameters`` tab

    * **Params**

      * **Key**
      * **Value**
    * **Texts**:  Translatable parameters
    * **Secrets**: Parameters with restricted access: key values are visible for Administrators only

  * In the ``Evaluation Context`` tab

    * **Evaluation context**: predefined additional variables and methods
    * **Common_code**: code that is executed before running any
      project's task. Can be used for initialization or for helpers. Any variables
      and functions that don't start with underscore symbol will be available in
      task's code.

  * In the ``Available Tasks`` tab

    * **Name**, e.g. *Sync products*
    * **Code**: code with at least one of the following functions

      * ``handle_cron()``
      * ``handle_db(records)``

        * ``records``: all records on which this task is triggered

      * ``handle_webhook(httprequest)``

        * ``httprequest``: contains information about request, e.g.

          * `httprequest.data <https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseRequest.data>`__: request data
          * `httprequest.files <https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseRequest.files>`__: uploaded files
          * `httprequest.remote_addr <https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseRequest.remote_addr>`__: ip address of the caller.
          * see `Werkzeug doc
            <https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseRequest>`__
            for more information.
        * optionally can return data as a response to the webhook request; any data transferred in this way are logged via ``log_transmission`` function:

          * for *json* webhook:
            * ``return json_data``
          * for *x-www-form-urlencoded* webhook:
            * ``return data_str``
            * ``return data_str, status``
            * ``return data_str, status, headers``

              * ``status`` is a response code, e.g. ``200``, ``403``, etc.
              * ``headers`` is a list of key-value tuples, e.g. ``[('Content-Type', 'text/html')]``
      * ``handle_button()``

    * **Cron Triggers**, **DB Triggers**, **Webhook Triggers**, **Manual
      Triggers**: when to execute the Code. See below for further information

Job Triggers
============

Cron
----

* **Trigger Name**, e.g. ``NIGHTLY_SYNC``
* **Execute Every**: every 2 hours, every 1 week, etc.
* **Next Execution Date**
* **Scheduler User**

DB
--

* **Trigger Name**, e.g. ``PRODUCT_PRICE_CHANGE``
* **Model**
* **Trigger Condition**

  * On Creation
  * On Update
  * On Creation & Update
  * On Deletion
  * Based on Timed Condition

    * Allows to trigger task before, after on in time of Date/Time fields, e.g.
      1 day after Sale Order is closed

* **Apply on**: records filter
* **Before Update Domain**: additional records filter for *On Update* event
* **Watched fields**: fields list for *On Update* event

Webhook
-------

* **Trigger Name**, e.g. ``ON_EXTERNAL_UPDATE``
* **Webhook Type**: *application/x-www-form-urlencoded* or *application/json*

* **Webhook URL**: readonly.

Button
------

* **Trigger Name**, e.g. ``SYNC_ALL_PRODUCTS``

Code
====

Available variables and functions:
----------------------------------

Base
~~~~

* ``env``: Odoo Environment
* ``log(message, level=LOG_INFO)``: logging function to record debug information

  log levels:

  * ``LOG_DEBUG``
  * ``LOG_INFO``
  * ``LOG_WARNING``
  * ``LOG_ERROR``
  *

* ``log_transmission(recipient_str, data_str)``: report on data transfer to external recipients

Links
~~~~~

* ``<record>.set_link(relation_name, external, sync_date=None, allow_many2many=False) -> link``: makes link between Odoo and external resource

  * ``allow_many2many``: when False raises an error if there is a link for the
    ``record`` and ``relation_name`` or if there is a link for ``relation_name``
    and ``external``;

* ``<records>.search_links(relation_name) -> links``
* ``get_link(relation_name, external_ref) -> link``

Odoo Link usage:

* ``link.odoo``: normal Odoo record

  * ``link.odoo._name``: model name, e.g. ``res.partner``
  * ``link.odoo.id``: odoo record id
  * ``link.odoo.<field>``: some field of the record, e.g. ``link.odoo.email``: partner email

* ``link.external``: external reference, e.g. external id of a partner
* ``link.sync_date``: last saved date-time information
* ``links.odoo``: normal Odoo RecordSet
* ``links.external``: list of all external references
* ``links.sync_date``: minimal data-time among links
* ``links.update_links(sync_date=None)``: set new sync_date value; if value is not passed, then ``now()`` is used
* ``links.unlink()``: delete links
* ``for link in links:``: iterate over links
* ``if links``: check that link set is not empty
* ``len(links)``: number of links in the set
* sets operations:

  * ``links1 == links2``: sets are equal
  * ``links1 - links2``: links that are in first set, but not in another
  * ``links1 | links2``: union
  * ``links1 & links2``: intersection
  * ``links1 ^ links2``: equal to ``(links1 | links2) - (links1 & links2)``



You can also link external data with external data on syncing two different system (e.g. github and trello).

* ``set_link(relation_name, {"github": github_issue_num, "trello": trello_card_num}, sync_date=None, allow_many2many=False) -> elink``
  * ``refs`` is a dictionary with system name and references pairs, e.g.

    .. code-block:: python

      {
        "github": github_issue_num,
        "trello": trello_card_num,
      }

* ``search_links(relation_name, refs) -> elinks``:
  * ``refs`` may contain list of references as values, e.g.

    .. code-block:: python

      {
        "github": [github_issue_num],
        "trello": [trello_card_num],
      }

  * use None values to don't filter by reference value of that system, e.g.

    .. code-block:: python

      {
        "github": None,
        "trello": [trello_card_num],
      }

  * if references for both systems are passed, then elink is added to result
    only when its references are presented in both references lists
* ``get_link(relation_name, refs) -> elink``

  * At least one of the reference should be not Falsy
  * ``get_link`` raise error, if there are few odoo records linked to the
    references. Set work with multiple relations (*one2many*, *many2one*,
    *many2many*) use ``set_link(..., allow_many2many=False)`` and
    ``search_links``

In place of ``github`` and ``trello`` you can use other labels depending on what you sync.

External Link is similar to Odoo link with the following differences:

* ``elink.get(<system>)``, e.g. ``elink.get("github")``: reference value for system; it's a replacement for ``link.odoo`` and ``link.external`` in Odoo link

Sync Helpers
~~~~~~~~~~~~

For one2one syncronization you can use following helpers.

* ``sync_odoo2x(src_list, sync_info, create=False, update=False)``

  * ``sync_info["x"]["create"](odoo_record) -> external_ref``: create external record and return reference
  * ``sync_info["x"]["update"](external_ref, odoo_record) -> external_ref``: update external record
  * ``sync_info["x"]["get_ref"](x)``: get reference for an item in src_list

* ``sync_x2odoo(src_list, sync_info, create=False, update=False)``

  * ``sync_info["odoo"]["create"](x) -> odoo_record``: create odoo record from external data
  * ``sync_info["odoo"]["update"](odoo_record, x) -> odoo_record``:  update odoo record according to providing external data

Common args:

* ``sync_info["relation"]``: same as ``relation_name`` in ``set_link``, ``get_link``
* ``src_list``: iterator of ``x`` or ``odoo_record`` values
*  ``create``: boolean value for "create record if it doesn't exist"
*  ``update``: boolean value for "update record if it exists"

To use helpers, create ``sync_info`` with all information, e.g.

.. code-block:: python

     EMPLOYEE_SYNC = {
       "relation": "my_system_and_odoo_employee_rel",
       "x": {
         "get_ref": employee2ref,
         "create": employee_create,
         "update": employee_update,
       },
       "odoo": {
         "create": employee_create_odoo,
         "update": employee_update_odoo,
       }
     }

Then you can reuse in all syncronizations, e.g.

.. code-block:: python

    # on initial fetching records from external system
    sync_x2odoo(all_employees_x, EMPLOYEE_SYNC, create=True)

    # to push all updates to external system
    sync_odoo2x(all_employees_odoo, EMPLOYEE_SYNC, update=True)

    # on updating a single record push all updates to external system
    sync_odoo2x([employee_odoo], EMPLOYEE_SYNC, update=True)


There is a similar helper for syncronization between two external systems:

* ``sync_external(src_list, relation, src_info, dst_info, create=False, update=False)``

  * ``src_info["get_ref"](src_data)``: get reference for an item in src_list
  * ``src_info["system"]``: e.g. ``"github"``
  * ``src_info["update"](dst_ref, src_data)``
  * ``src_info["create"](src_data) -> dst_ref``
  * ``dst["system"]``: e.g. ``"trello"``

Project Values
~~~~~~~~~~~~~~

* ``params.<PARAM_NAME>``: project params
* ``webhooks.<WEBHOOK_NAME>``: contains webhook url; only in tasks' code

Event
~~~~~

* ``trigger_name``: available in tasks' code only
* ``user``: user related to the event, e.g. who clicked a button

Asynchronous work
~~~~~~~~~~~~~~~~~

* ``add_job(func_name, **options)(*func_args, **func_kwargs)``: call a function asynchronously; options are similar to ``with_delay`` method of ``queue_job`` module:

  * ``priority``: Priority of the job, 0 being the higher priority. Default is 10.
  * ``eta``: Estimated Time of Arrival of the job. It will not be executed before this date/time.
  * ``max_retries``: maximum number of retries before giving up and set the job
    state to 'failed'. A value of 0 means infinite retries. Default is 5.
  * ``description`` human description of the job. If None, description is
    computed from the function doc or name
  * ``identity_key`` key uniquely identifying the job, if specified and a job
    with the same key has not yet been run, the new job will not be added.

Libs
~~~~

* ``json``
* ``time``
* ``datetime``
* ``dateutil``
* ``timezone``
* ``b64encode``
* ``b64decode``

Tools
~~~~~

* ``url2base64``
* ``get_lang(env, lang_code=False)``: returns `res.lang` record
* ``html2plaintext``
* ``type2str``: get type of the given object
* ``DEFAULT_SERVER_DATETIME_FORMAT``

Exceptions
~~~~~~~~~~

* ``UserError``
* ``ValidationError``
* ``RetryableJobError``: raise to restart job from beginning; e.g. in case of temporary errors like broken connection
* ``OSError``

Evaluation context
------------------

Evaluation provides additional variables and methods for a project. For example, for telegram integration is could be method to send message to a telegram user. To make such additional context, you need to make a new module and make extension for ``sync.project`` model. Example:

.. code-block:: python

   import requests
   from odoo import api, fields, models

   class SyncProject(models.Model):

       _inherit = "sync.project"
       eval_context = fields.Selection(selection_add=[
           ("my_project", "My Project"),
       ])

       @api.model
       def _eval_context_my_project(self, secrets, eval_context):
           """Additional function to make http request

           * httpPost(url, **kwargs)
           """
           log_transmission = eval_context["log_transmission"]
           log = eval_context["log"]
           def httpPOST(url, **kwargs):
               log_transmission(url, json.dumps(kwargs))
               r = requests.request("POST", url, **kwargs)
               log("Response: %s" % r.text)
               return r.text
           return {
               "httpPost": httpPost
           }

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

Demo Project: Odoo <-> Telegram
===============================

In this project we create new partners and attach messages sent to telegram bot.
Odoo Messages prefixed with ``/telegram`` are sent back to telegram.

To try it, you need to install this module in demo mode. Also, your odoo
instance must be accessible over internet to receive telegram webhooks. Due to
telegram requirements, your web server must use `https` connection.

How it works
------------

*Webhook Trigger* waits for an update from telegram. Once it happened, the action depends on message text:

* for ``/start`` message (it's sent on first bot usage), we reply with welcome
  message (can be configured in project parameter TELEGRAM_WELCOME_MESSAGE) and
  create a partner with **Internal Reference** equal to *<TELEGRAM_USER_ID>@telegram*

* for any other message we attach a message copy to the partner with corresponding **Internal Reference**

*DB trigger* waits for a message attached to a telegram partner (telegram partners are filtered by **Internal Reference** field). If the message has ``/telegram`` prefix, task's code is run:

* a message copy (after removing the prefix) is sent to corresponding telegram user
* attach report message to the partner record

Configuration
-------------

In Telegram:

* send message ``/new`` to @BotFather and follow further instructions to create bot and get the bot token

In Odoo:

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Parameters >> System Parameters``
* Check that parameter ``web.base.url`` is properly set and it's accessible over
  internet (it should not localhost). Also, telegram accepts https addresses only (i.e. not http)
* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Demo Telegram Integration* project
* Go to ``Parameters`` tab
* Set **Secrets**:

  * TELEGRAM_BOT_TOKEN

* Unarchive the project
* Open *Manual Triggers* Tab
* Click button ``[Run Now]`` near to *Setup* task

Usage
-----

In Telegram:

* send some message to the created bot

In Odoo:

* Open Contacts/Customers menu
* RESULT: there is new partner with name *Telegram:<YOUR TELEGRAM NAME>* (the prefix can be configured in project parameter PARTNER_NAME_PREFIX)
* Open the partner and attach a log/message with prefix ``/telegram``, e.g. ``/telegram Hello! How can I help you?``
* Wait few seconds to get confirmation
* RESULT: you will see new attached message from Odoo Bot with confirmation that message is sent to telegram

In telegram:

* RESULT: the message is delivered via bot

You can continue chatting in this way

Demo Project: Odoo2odoo
=======================

In this project we push partners to external Odoo 13.0 and sync back avatar changes.

To try it, you need to install this module in demo mode.

How it works
------------

*DB trigger* waits for partner creation. When it happens, task's code is run:

* creates a copy of partner on external Odoo

  * XMLRPC is used as API

* gets back id of the partner copy on external Odoo
* attaches the id to the partner of our Odoo via ``set_link`` method

To sync changes on external Odoo we use *Cron trigger*. It runs every 15 minutes. You can also run it manually. The code works as following:

* call ``search_links`` function to get ids to sync and the oldest sync date
* request to the external Odoo for the partners, but filtered by sync time to don't load partner without new updates
* for each of the fetched partner compare its update time with sync date saved in the link

  * if a partner is updated since last sync, then update partner and sync date

Configuration
-------------

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Demo Odoo2odoo integration* project
* Go to ``Parameters`` tab
* Set **Params**:
  * URL, e.g. ``https://3674665-12-0.runbot41.odoo.com``
  * DB, e.g. ``odoo``
* Set **Secrets**:

  * USERNAME, e.g. ``admin``
  * PASSWORD, e.g. ``admin``
* Unarchive the project

Usage
-----

**Syncing new partner.**

* Open Contacts/Customers menu
* Create new partner
* Go back to the project
* Click ``Logs`` button and check that there are no errors

* Open the external Odoo

  * RESULT: the partner copy is on the external Odoo
  * Update avatar image on it

* Go back to the *Demo Odoo2odoo Integration* project in our Odoo
* Click ``Available Tasks`` tab
* Click ``[Edit]``
* Go to ``Sync Remote Partners Updates`` task
* Click on ``Available Triggers`` tab and go inside ``CHECK_EXTERNAL_ODOO`` trigger
* Configure cron
* Make trigger Active on the upper right corner
* Click ``[Save]``

* Then you can trigger synchronization in some of the following ways:

  1. Click ``[Run Manually]`` inside the trigger

  2. Simply wait up to cron job will start on a schedule :)

* Now open the partner in our Odoo
* RESULT: avatar is synced from external Odoo
* You can try to change avatar on external Odoo again and should get the same results

**Uploading all existing partners.**

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Demo Odoo2odoo Integration* project
* Choose Sync Task *Sync Local Partners To Remote Odoo*
* Click button ``[Run Now]``
* Open the external Odoo

  * RESULT: copies of all our partners are in the external Odoo; they have *Sync Studio:* prefix (can be configured in project parameter UPLOAD_ALL_PARTNER_PREFIX)

Demo project: GitHub <-> Trello
===============================

In this project we create copies of github issues/pull requests and their
messages in trello cards. It's one side synchronization: new cards and message in
trello are not published in github. Trello and Github labels are
synchronized in both directions.

To try it, you need to install this module in demo mode. Also, your odoo
instance must be accessible over internet to receive github and trello webhooks.

How it works
------------


*Github Webhook Trigger* waits from GitHub for issue creation and new messages:

* if there is no trello card linked to the issue, then create trello card and link it with the issue
* if new message is posted in github issue, then post message copy in trello card

*Github Webhook Trigger* waits from GitHub for label attaching/detaching (*Trello Webhook Trigger* works in the same way)

* if label is attached in GitHub issue , then check for github label and trello
  label links and create trello label if there is no such link yet
* if label is attached in github issue, then attach corresponding label in trello card
* if label is detached in github issue, then detach corresponding label in trello card

*Github Webhook Trigger* waits from GitHub for label updating/deleting (*Trello Webhook Trigger* works in the same way):

* if label is changed and there is trello label linked to it, then update the label
* if label is changed and there is trello label linked to it, then delete the label

There is still possibility that labels are mismatch, e.g. due to github api
temporary unavailability or misfunction (e.g. api request to add label responded
with success, but label was not attached) or if odoo was stopped when github
tried to notify about updates. In some cases, we can just retry the handler
(e.g. there was an error on api request to github/trello, then the system tries
few times to repeat label attaching/detaching). As a solution for cases when
retrying didn't help (e.g. api is still not working) or cannot help (e.g. odoo
didn't get webhook notification), we run a *Cron Trigger* at night to check for
labels mismatch and synchronize them. In ``LABELS_MERGE_STRATEGY`` you can
choose which strategy to use:

* ``USE_TRELLO`` -- ignore github labels and override them with trello labels
* ``USE_GITHUB`` -- ignore trello labels and  override them with push github labels
* ``UNION`` -- add missed labels from both side
* ``INTERSECTION`` -- remove labels that are not attached on both side

Configuration
-------------

* Open menu ``[[ Sync Studio ]] >> Sync Projects``
* Select *Demo Github-Trello Integration* project
* In ``Parameters`` tab set **Secrets** (check Description and Documentation links near the parameters table about how to get the secret parameters):

  * ``GITHUB_REPO``
  * ``GITHUB_TOKEN``
  * ``TRELLO_BOARD_ID``
  * ``TRELLO_KEY``
  * ``TRELLO_TOKEN``

* In *Available Tasks* tab:

  * Click ``[Edit]``
  * Open *Labels Conflict resolving* task
  * In *Available Triggers* tab:

    * Open *CONFLICT_RESOLVING* Cron
    * Change **Next Execution Date** in webhook to the night time
    * Set **Number of Calls**, a negative value means no limit (e.g. `-1`)
    * Make it active by checking the box in front of the corresponding field
    * Click ``[Save]``
* Save all the changes you made in the integration
* Make integration Active by clicking ``Action >> Unarchive``
* In project's *Manual Triggers* tab:

  * Click ``[Run Now]`` buttons in trigger *SETUP_GITHUB*
  * Click ``[Run Now]`` buttons in triggers *SETUP_TRELLO*. Note, that `it doesn't work <https://github.com/odoo/odoo/issues/57133>`_ without one of the following workarounds:

    * open file ``sync/controllers/webhook.py`` and temporarily change ``type="json"`` to ``type="http"``. Revert the changes after successfully setting up trello
    * add header "Content-Type: application/json" via your web server. Example for nginx:

      .. code-block:: nginx

        location /website/action-json/ {
            return 200 "{}";
        }


  * After a successful *SETUP_TRELLO* trigger run, return everything to its original position, otherwise the project will not work correctly



Usage
-----

**Syncing new Github issue**

* Open Github
* Create issue
* Open trello
* RESULT: you see a copy of the Github issue
* Go back to the Github issue
* Post a message
* Now go back to the trello card
* RESULT: you see a copy of the message
* You can also add/remove github issue labels or trello card labels (note that the name of the label must be added
  in Trello so that there are no errors in the GitHub).

  * RESULT: once you change them on one side, after short time, you will see the changes on another side

**Labels syncing**

* Open Github or Trello
* Rename or delete some label
* RESULT: the same happened in both systems

**Conflict resolving**

* Create a github issue and check that it's syncing to trello
* Stop Odoo
* Make *different* changes of labels both in github issue and trello card
* Start Odoo
* Open menu ``[[ Sync Studio ]] >> Projects``
* Select *Demo Trello-Github integration* project
* Click ``[Edit]`` and open *Labels Conflict Resolving* task in *Available Tasks* tab
* Make ``CONFLICT_RESOLVING`` Cron Trigger run in one of the following ways

  1. Choose Cron Trigger and click ``[Run Manually]``

  2. Change **Next Execution Date** to a past time and wait up to 1 minute

* RESULT: the github issue and corresponding trello card the same set of labels. The merging is done according to selected strategy in ``LABELS_MERGE_STRATEGY`` parameter.


**Syncing all existing Github issues.**

* Open menu ``[[ Sync Studio ]] >> Projects``
* Select *Demo Tello-Github Integration* project
* Click button ``[Run Now]`` near to ``PUSH_ALL_ISSUES`` manual trigger
* It will start asynchronous jobs. You can check progress via button *Jobs*
* After some time open Trello

  * RESULT: copies of all *open* github issues are in trello; they have *GITHUB:* prefix (can be configured in project parameter ISSUE_FROM_GITHUB_PREFIX)

Custom Integration
==================

If you made a custom integration via UI and want to package it into a module,
open the Sync Project and click ``[Actions] -> Export to XML`` button.
