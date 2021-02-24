==========
 Base Api
==========

Usage
=====

*Methods intended for calling via API (e.g. OpenAPI or RPC)*:

search_or_create
----------------

*search_or_create(self, vals, active\_test=True)*

*– Purpose*:
  - To resolve “race conditions”, comparing to separated searching
    and creation, that can lead to record-duplication.

*– Input data*:
  - `vals`-variable:
      - fields-values as for *create*-method
      - type of dictionary (not nested)
      - e.g.
            .. code-block::

                vals = {
                        'name': 'John',
                        'Age': 25
                        }

  - `active_test`-variable (for models that have field named `active`):
      - flag to search only for *active* records
      - type of *boolean*
      - e.g.
            .. code-block::

                 active_test = False`  # to also search in *in-active* records

*– Notes*:
  - *many2one* fields in `vals`:
      - type of integer
      - e.g.
            .. code-block::

                vals = {
                        'company_id': 1
                       }

  - *x2many* fields in `vals`:
      - ignored for searching
      - type of list of *tuples*
      - e.g.
            .. code-block::

                vals = {
                            'name': John',
                            'children_ids': [(4,4,0),
                                             (4,5,0)]
                        }
      - For more information look `here <https://odoo-development.readthedocs.io/en/latest/dev/py/x2many.html>`__

*– Example*:

.. code-block::

  -> # Searching for existing record

  -> vals = {'company_id': 1 }

  -> res_partner_object.search_or_create(vals)

  (False, [22, 1, 8, 7, 3])

  -> # Creating record (with many2one field)

  -> vals = { 'name': 'John Doe Neo', 'company_id': 1 }

  -> res_partner_object.search_or_create(vals)

  (True, [78])

  -> # Creating record (for x2many-fields)

  -> vals = { 'name': 'Albert Bubis', 'child_ids': [(4, 11, 0), (4, 5, 0)] }

  -> res_partner_object.search_or_create(vals)

  (True, [79])

*– Algorithm*:

1.  Creates *domain* out of `vals` for searching

2.  Searches for records satisfiy *domain* constraints (`is_new = False`)

3.  If no record was found:
      - then it creates one with `vals`
      - sets *True* to `is_new`

4.  Returns two variables:
      - `is_new` - *boolean*: Shows if record was created or not
      - `ids` - list of records, that were found, or id of created
        one

search_read_nested
------------------

*search_read_nested(self, domain=None, fields=None, offset=0, limit=None, order=None, delimeter='/')*

*– Purpose*:
  - Simplifies reading data to one request;
  - Comparing to default **search\_read**:
      - ``fields`` can be nested, so the method will return list of
        record-dictionaries with nested fields from related models (via
        *x2many*, *many2one*). Nested fields are specified as slash-separated
        sequence, for example:
          .. code-block::

             fields = [
                 'company_id/id',
                 'company_id/name'
             ]

*– Input data*:
  - `domain`-variable:
      - list of statements for searching, as for usual
        *search*-method
      - type of list of *tuples*
      - e.g. 
          .. code-block::

            domain = [
                        ('name', '=', 'John'),
                        ('Age','>','10')
                    ]

  - `fields`-variable:
      - fields to be read from founded records (including nested
        fields via dot-notation)
      - list of *strings*
      - e.g. if ``author_id``, ``edition_ids`` are many2one and many2many
        fields, then the variable can be specified as following:
          .. code-block::

            fields = [
                'book_name',
                'author_id/id',
                'author_id/name',
                `edition_ids/id`,
                `edition_ids/year`
            ]

  - `offset`-variable:
      - number of records to ignore
      - type of *integer*
      - e.g. ``offset = 2`` # will ignore two first-founded records
  - `limit`-variable:
      - number of founded records to show
      - type of
      - e.g. ``limit = 3`` # will show three first-founded records
  - `order`-variable:
      - criteria of sorting founded records
      - type of *string*
      - e.g. ``order = 'name desc'`` # will sort records descending by ‘name’
  - `count`-variable:
      - flag to return number of founded records, instead of records
        itself
      - type of *boolean*
      - e.g. ``count = True``
  - `delimeter`-variable:
      - char that divide nesting in field
      - type of *char*
      - e.g. ``company_id/country_id/name # delimeter='/'

*– Notes*:
  - for *many2one* fields the method returns a dictionary with
    nested fields
  - for *x2many* fields the method returns list of
    record-dictionaries with nested fields

*– Example*

.. code-block::

  -> search_domain = [('company_id.category', '=', 'Supermarket')]

  -> show_fields = [ 'name', 'company_id/id', 'company_id/name', 'company_id/website', 'country_id/id', 'child_ids/name', 'child_ids/id' ]

  -> res_partner_object.search_read_nested(domain=search_domain, fields=show_fields, '.')

  [
      {

          'name': 'Partner #1',

          'company_id': {
                          'id': 1,
                          'name': 'Supermarket for me',
                          'website': 'http://superfood.com'
                          },

          'country_id': { 'id':102' },

          'child_ids': [
                          {
                              'id': 1,
                              'name': Child #1,
                          }, {
                              'id': 2,
                              'name': Child #2,
                          }
                      ]

      },

      ...,

      {

          'name': 'Partner #37',

          'company_id': {
                          'id': 25,
                          'name': 'Supermarket in Eternity',
                          'website': 'http://giantbroccoly.com'
                          },

          'country_id': { 'id': 103 }

          'child_ids': []

      }
  ]


*– Algorithm*:
  1. Searches for records that satisfy `domain`

  2. Returns list of dictionaries with fields specified in `fields`

create_or_update_by_external_id
-------------------------------

*create_or_update_by_external_id(self, vals)*

*– Purpose*:
  - work with model (create or update values) by custom (external)
    identification

*– Input data*:
  - `vals`-variable:
      - type of *dictionary* as for *create*-method
      - Must contain `id` field type of *string*
      - e.g.
            .. code-block::

               vals = {
                        'id': 'ext.id_1',
                        'name: 'John',
                        'age': 37,
                        'job_id': 'ext.work_1',
                        'child_ids' : [
                                       (4, 'ext.child_1', 0),
                                       (4, 'ext.child_2', 0)
                                      ]
                      }`

*– Notes*:
  - for *x2x*-fields `id` might be *string* (external id)

  - for *x2many*-fields use *tuples* `this <https://odoo-development.readthedocs.io/en/latest/dev/py/x2many.html>`__,

  - If `id` of *x2x* fields are not found, it will return error
    (*raise Exception*). In order to avoid this, call the function
    for the models of this fields

  - Work of function based on *External Identifiers* (**ir.model.data** )

*– Example*

.. code-block::

  -> # Create non-existed record

  -> vals = {
              'id': 'ext.id_5',
              'name': 'John',
              'customer_id': 'ext.id_3',
              'child_ids': [(4, 'ext.id_child_5, 0), (4, 5, 0)]
          }

  -> sale_order_object.create_or_update_by_external_id(vals)

      (True, 38)

  -> # Update existing record

  -> vals = {
              'id': 'ext.id_5',
              'customer_id': 'ext.id_5',
              'child_ids': [(4, 'ext.id_child_4', 0)]
          }

  -> sale_order_object.create_or_update_by_external_id(vals)

      (False, 38)

*– Algorithm*:
  - Searches for record by its external id (`id` in `vals`) through
    *self.env.ref*-function
  - If no record was found:
      - then it creates one with requested values (`vals`)
      - register `id` of `vals` in **ir.model.data**
      - sets *True* to `is_new`
  - Returns two variables:
      - `is_new` - *True* or *False*: if record was created or not
      - `id` (inner) of updated or created record
