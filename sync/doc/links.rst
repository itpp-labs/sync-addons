This document describes Sync Studio tools that help linking records between resources (internal and external).

* ``<record>.set_link(relation_name, external, sync_date=None, allow_many2many=False) -> link``: makes link between Odoo and external resource

  * ``allow_many2many``: when False raises an error if there is a link for the
    ``record`` and ``relation_name`` or if there is a link for ``relation_name``
    and ``external``;

* ``<records>.search_links(relation_name) -> links``
* ``MAGIC.get_link(relation_name, external_ref, model=None) -> link``

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

* ``MAGIC.set_link(relation_name, {"github": github_issue_num, "trello": trello_card_num}, sync_date=None, allow_many2many=False, model=None) -> elink``
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
* ``get_link(relation_name, refs, model=None) -> elink``

  * At least one of the reference should be not Falsy
  * ``get_link`` raise error, if there are few odoo records linked to the
    references. Set work with multiple relations (*one2many*, *many2one*,
    *many2many*) use ``set_link(..., allow_many2many=False)`` and
    ``search_links``

In place of ``github`` and ``trello`` you can use other labels depending on what you sync.

External Link is similar to Odoo link with the following differences:

* ``elink.get(<system>)``, e.g. ``elink.get("github")``: reference value for system; it's a replacement for ``link.odoo`` and ``link.external`` in Odoo link
