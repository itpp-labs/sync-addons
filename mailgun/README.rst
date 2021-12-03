.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

=========
 Mailgun
=========

With this module you can receive incoming messages from mailgun.
There is no IMAP or POP3 servers on mailgun that is to be used with odoo.
That is why we need this module. It fetches messages from mailgun using their API
and stores them in odoo.

TODO
====

* If emails are sent when odoo is stopped then Mailgun will retry (other than for delivery notification) during 8 hours at the following intervals before stop trying: 10 minutes, 10 minutes, 15 minutes, 30 minutes, 1 hour, 2 hour and 4 hours. This could be fixed by fetching undelivered messages after odoo starts.

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* Ildar Nasyrov <Nasyrov@it-projects.info>
* Ivan Yelizariev <yelizariev@it-projects.info>

Further information
===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/9.0/mailgun/


Tested on `Odoo 9.0 <https://github.com/odoo/odoo/commit/c8cd67c5d98b410cabe0a6efb3347a8a4de731d8>`_
