=========
 Mailgun
=========

Usage
=====

* register or log in http://mailgun.com
* On https://mailgun.com/app/domains click on you domain, e.g. sandbox123...mailgun.org domain. Here you can see all information needed to configure odoo outgoing mail feature

  * if you in sandbox domain, add Authorized Recepient
  * Copy API Key value into odoo

    * Open menu ``Settings / Parameters / System Parameters``
    * Create new parameter

      * key: ``mailgun.apikey``
      * Value: API Key from mailgun (``key-...``)
      * click Save

  * Copy smtp credentials into odoo

    * open ``Settings / Technical / Email / Outgoing Mail Servers``

      * delete localhost
      * create new server

        * Description: ``mailgun``
        * SMTP Server: ``smtp.mailgun.org``
        * Connection Security: ``SSL/TLS``
        * Username: e.g. ``postmaster@sandbox123....mailgun.org``
        * Password: ``...`` (copy ``Default Password`` from mailgun)

  * From odoo menu ``Settings / General Settings`` edit Alias Domain

    * Put your mailgun domain here. E.g. sandbox123...mailgun.org
    * Click 'Apply' button

* From https://mailgun.com/cp/routes create new route

  * Priority: ``0``
  * Filter expression: ``catch_all()``
  * Actions: ``store(notify="http://<your odoo domain>/mailgun/notify")``

* Set admin's email alias. Open menu ``Settings / Users / Users``

  * choose your user and click ``[Edit]``
  * On Preference tab put alias into Messaging Alias field and click ``[Save]``. E.g. ``admin@sandbox...mailgun.org``

* Via your favorite mail client (e.g. gmail.com) send email to ``admin@sandox...mailgun.org``
* Open ``Discuss`` in odoo
* See your message there
* Reply to the message and check it in your mail client (e.g. gmail.com)
