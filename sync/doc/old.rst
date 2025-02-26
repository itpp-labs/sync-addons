Demo Project: Odoo2odoo (obsolete)
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
  * URL, e.g. ``https://odoo.example``
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

Demo project: GitHub <-> Trello (obsolete)
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

    * delete `line <https://github.com/odoo/odoo/blob/db25a9d02c2fd836e05632ef1e27b73cfdd863e3/odoo/http.py#L326>`__ that raise exception in case of type mismatching (search for ``Function declared as capable of handling request of type`` in standard Odoo code). In most cases, this workaround doesn't need to be reverted
    * open file ``sync/controllers/webhook.py`` and temporarily change ``type="json"`` to ``type="http"``. Revert the changes after successfully setting up trello
    * Add a temporal handler in your proxy/web server. Example for nginx:

      .. code-block:: nginx

        location /website/action-json/ {
            return 200 "{}";
        }

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

Custom Integration (obsolete)
==================

If you made a custom integration via UI and want to package it into a module,
open the Sync Project and click ``[Actions] -> Export to XML`` button.
