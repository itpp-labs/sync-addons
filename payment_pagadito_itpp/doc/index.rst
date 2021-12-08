===========================
 Pagadito Payment Acquirer
===========================

Preparation
===========

* You will need account at https://www.pagadito.com/
* Nagivate to pagadito dashboard. Check that you have access to *integration parameters* section.

  * Under *Connection Credentials* you can find **UID** and **WSK**
  * **Return URL** -- set to ``<odoo_instance_url>/payment/pagadito/confirmation?value={value}&ern_value={ern_value}``, e.g. ``myshop.example.com/payment/pagadito/confirmation?value={value}&ern_value={ern_value}``

Sandbox
=======

You can play with a module via sandbox account created on this website: https://sandbox.pagadito.com.

If you get error "¡Lo sentimos! Pagadito Comercios aún no está disponible en su país o región" (Pagadito is not supported in your country), contact support team to add your IP to whilelist

Installation
============

Install `zeep <https://python-zeep.readthedocs.io/en/master/>`__ library:

    pip install zeep


Configuration
=============

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Parameters >> System Parameters``
* Check that parameter``web.base.url`` exists and has correct address for eCommerce website.
* Open menu ``[[ Invoicing ]] >> Configuration >> Payments >> Payment Acquirers``
* Select *Pagadito* record and set following parameters:

  * **UID** -- *El identificador del Pagadito Comercio*.
  * **WSK**  --  *La clave de acceso*
* Optionally, click ``[Unpublished On Website]`` button to allow pagadito at eCommerce

Mail notification
-----------------
Pagadito requires to send confirmation codes by email. In order to do that:

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Email >> Templates``
* Open template ``Sales Order - Send by Email``
* Click ``[Edit]``
* Switch editor to *Code View* via button ``</>``
* Add following code in a proper place, e.g. before the line ``<p>You can reply to this email if you have any questions.</p>``

    % if object.payment_acquirer_id.provider == 'pagadito':
        <p>
        Pagadito Payment confirmation codes: NAP=${object.payment_tx_id.acquirer_reference}, ERN=${object.payment_tx_id.reference}
        </p>
    % endif

* Click ``[Save]``

Usage
=====

eCommerce
---------
* install ``website_sale`` module
* add a product to the cart
* checkout the order and select *Pagadito* as payment method
* proceed the payment at pagadito website
* RESULT: payment is done and processed at odoo backend
