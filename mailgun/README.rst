=========
 Mailgun
=========

With this module you can receive incoming messages from mailgun.
There is no IMAP or POP3 servers on mailgun that is to be used with odoo.
That is why we need this module. It fetches messages from mailgun using their API
and stores them in odoo.

TODO
----

* If emails are sent when odoo is stopped then Mailgun will retry (other than for delivery notification) during 8 hours at the following intervals before stop trying: 10 minutes, 10 minutes, 15 minutes, 30 minutes, 1 hour, 2 hour and 4 hours. This could be fixed by fetching undelivered messages after odoo starts.

Credits
=======

Contributors
------------
* Ildar Nasyrov <Nasyrov@it-projects.info>
* Ivan Yelizariev <yelizariev@it-projects.info>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`_

Further information
===================

HTML Description: https://apps.odoo.com/apps/modules/9.0/mailgun/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 9.0 c8cd67c5d98b410cabe0a6efb3347a8a4de731d8
