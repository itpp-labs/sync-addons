This document describes `MAGIC.*` tools available on Project Code evaluation (core code, library code, task code)


Base
====

* ``MAGIC.env``: Odoo Environment
* ``MAGIC.log(message, level=MAGIC.LOG_INFO)``: logging function to record debug information

  log levels:

  * ``MAGIC.LOG_DEBUG``
  * ``MAGIC.LOG_INFO``
  * ``MAGIC.LOG_WARNING``
  * ``MAGIC.LOG_ERROR``

* ``MAGIC.log_transmission(recipient_str, data_str)``: report on data transfer to external recipients

Links
=====

* ``MAGIC.get_link(...)``
* ``MAGIC.set_link(...)``

These methods are documented separetely in `<links.rst>`__.

Sync Helpers
============

* ``MAGIC.sync_odoo2x(...)``
* ``MAGIC.sync_x2odoo(...)``
* ``MAGIC.sync_external(...)``

These methods are documented separetely in `<sync.rst>`__.

Event
=====

* ``MAGIC.trigger_name``: available in tasks' code only
* ``MAGIC.user``: user related to the event, e.g. who clicked a button

Asynchronous work
=================

* ``MAGIC.add_job(func_name, **options)(*func_args, **func_kwargs)``: call a function asynchronously; options are similar to ``with_delay`` method of ``queue_job`` module:

  * ``priority``: Priority of the job, 0 being the higher priority. Default is 10.
  * ``eta``: Estimated Time of Arrival of the job. It will not be executed before this date/time.
  * ``max_retries``: maximum number of retries before giving up and set the job
    state to 'failed'. A value of 0 means infinite retries. Default is 5.
  * ``description`` human description of the job. If None, description is
    computed from the function doc or name
  * ``identity_key`` key uniquely identifying the job, if specified and a job
    with the same key has not yet been run, the new job will not be added.


Attachments
===========

* ``attachment._public_url()``:  generates access url. Can be used to pass attachments to an external system as url, instead of direct uploading the content.

Libs
====

* ``MAGIC.json``
* ``MAGIC.time``
* ``MAGIC.datetime``
* ``MAGIC.dateutil``
* ``MAGIC.timezone``
* ``MAGIC.b64encode``
* ``MAGIC.b64decode``

Tools
=====

* ``MAGIC.url2base64``
* ``MAGIC.url2bin``
* ``MAGIC.get_lang(env, lang_code=False)``: returns `res.lang` record
* ``MAGIC.html2plaintext``
* ``MAGIC.type2str``: get type of the given object
* ``MAGIC.DEFAULT_SERVER_DATETIME_FORMAT``
* ``MAGIC.AttrDict``: like a dictionary, but with accessing to attributes via dot.

Exceptions
==========

* ``MAGIC.UserError``
* ``MAGIC.ValidationError``
* ``MAGIC.RetryableJobError``: raise to restart job from beginning; e.g. in case of temporary errors like broken connection
* ``MAGIC.OSError``
