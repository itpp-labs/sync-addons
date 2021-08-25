.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

===================
 Viber Integration
===================

The module allows creating a Viber bot to communicate with people through Odoo.

For each Viber user, the module creates a partner with corresponding information (name, nickname, avatar).

Docs
====

https://developers.viber.com/docs/api/python-bot-api/

Limits on files sending
-----------------------------

* Files
  
  Some files format are forbidden: https://developers.viber.com/docs/api/rest-bot-api/#forbiddenFileFormats

* Photo
  
   The URL must have a resource with a .jpeg, .png or .gif file extension as the last path segment. 
   Example: http://www.example.com/path/image.jpeg. Animated GIFs can be sent as URL messages or file messages. 
   Max image size: 1MB on iOS, 3MB on Android.
   
* Video
   
   Max size 26 MB. Only MP4 and H264 are supported. 
   The URL must have a resource with a .mp4 file extension as the last path segment.


Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Further information
===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/14.0/sync_viber/


Notifications on updates: `via Atom <https://github.com/itpp-labs/sync-addons/commits/14.0/sync_viber.atom>`_, `by Email <https://blogtrottr.com/?subscribe=https://github.com/itpp-labs/sync-addons/commits/14.0/sync_viber.atom>`_

Tested on `Odoo 14.0 <https://github.com/odoo/odoo/commit/6916981f56783de7008cd04d4e37e80166150ff7>`_
