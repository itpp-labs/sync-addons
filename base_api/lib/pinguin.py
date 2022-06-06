# Copyright 2018, XOE Solutions
# Copyright 2018-2019 Rafis Bikbov <https://it-projects.info/team/bikbov>
# Copyright 2019 Yan Chirino <https://xoe.solutions/>
# Copyright 2019-2020 Anvar Kildebekov <https://it-projects.info/team/fedoranvar>
# Copyright 2020 Ivan Yelizariev
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
# pyling: disable=redefined-builtin


import collections
import collections.abc
import datetime

import six
import werkzeug.wrappers
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import odoo
from odoo.http import request

try:
    import simplejson as json
except ImportError:
    import json


# 4xx Client Errors
CODE__obj_not_found = (
    404,
    "Object not found",
    "This object is not available on this instance.",
)
# 5xx Server errors
CODE__invalid_spec = (
    501,
    "Invalid Field Spec",
    "The field spec supplied is not valid.",
)


def error_response(status, error, error_descrip):
    """Error responses wrapper.
    :param int status: The error code.
    :param str error: The error summary.
    :param str error_descrip: The error description.
    :returns: The werkzeug `response object`_.
    :rtype: werkzeug.wrappers.Response
    .. _response object:
        http://werkzeug.pocoo.org/docs/0.14/wrappers/#module-werkzeug.wrappers
    """
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps({"error": error, "error_descrip": error_descrip}),
    )


def validate_extra_field(field):
    """Validates extra fields on the fly.
    :param str field: The name of the field.
    :returns: None, if validated, otherwise raises.
    :rtype: None
    :raise: werkzeug.exceptions.HTTPException if field is invalid.
    """
    if not isinstance(field, str):
        return werkzeug.exceptions.HTTPException(
            response=error_response(*CODE__invalid_spec)
        )


def validate_spec(model, spec):
    """Validates a spec for a given model.
    :param object model: (:obj:`Model`) The model against which to validate.
    :param list spec: The spec to validate.
    :returns: None, if validated, otherwise raises.
    :rtype: None
    :raise: Exception:
                    * if the tuple representing the field does not have length 2.
                    * if the second part of the tuple representing the field is not a list or tuple.
                    * if if a tuple representing a field consists of two parts, but the first part is not a relative field.
                    * if if the second part of the tuple representing the field is of type tuple, but the field is the ratio 2many.
                    * if if the field is neither a string nor a tuple.
    """
    self = model
    for field in spec:
        if isinstance(field, tuple):
            # Syntax checks
            if len(field) != 2:
                raise Exception(
                    "Tuples representing fields must have length 2. (%r)" % field
                )
            if not isinstance(field[1], (tuple, list)):
                raise Exception(
                    """Tuples representing fields must have a tuple wrapped in
                    a list or a bare tuple as it's second item. (%r)"""
                    % field
                )
            # Validity checks
            fld = self._fields[field[0]]
            if not fld.relational:
                raise Exception(
                    "Tuples representing fields can only specify relational fields. (%r)"
                    % field
                )
            if isinstance(field[1], tuple) and fld.type in ["one2many", "many2many"]:
                raise Exception(
                    "Specification of a 2many record cannot be a bare tuple. (%r)"
                    % field
                )
        elif not isinstance(field, six.string_types):
            raise Exception(
                "Fields are represented by either a strings or tuples. Found: %r"
                % type(field)
            )


def update(d, u):
    """Update value of a nested dictionary of varying depth.
    :param dict d: Dictionary to update.
    :param dict u: Dictionary with updates.
    :returns: Merged dictionary.
    :rtype: dict
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, collections.OrderedDict([])), v)
        else:
            d[k] = v
    return d


# Transform string fields to dictionary
def transform_strfields_to_dict(fields_list, delim="/"):
    """Transform string fields to dictionary.
    Example:
    for ['name', 'email', 'bank_ids/bank_id/id', 'bank_ids/bank_name', 'bank_ids/id']
    the result will be the next dictionary
    {
        'name': None,
        'email': None
        'bank_ids': {
            'bank_name': None,
            'bank_id': {
                'id': None
            }
        },
    }
    :param list fields_list: The list of string fields.
    :returns: The dict of transformed fields.
    :rtype: dict
    """
    dct = {}
    for field in fields_list:
        parts = field.split(delim)
        data = None
        for part in parts[::-1]:
            if part == ".id":
                part = "id"
            data = {part: data}
        update(dct, data)
    return dct


def transform_dictfields_to_list_of_tuples(record, dct, ENV=False):
    """Transform fields dictionary to list.
    for {
        'name': None,
        'email': None
        'bank_ids': {
            'bank_name': None,
            'bank_id': {
                'id': None
            }
        },
    }
    the result will be
    ['name', 'email', ('bank_ids', ['bank_name', ('bank_id', ('id',))])]
    :param odoo.models.Model record: The model object.
    :param dict dct: The dictionary.
    :returns: The list of transformed fields.
    :rtype: list
    """
    fields_with_meta = {
        k: meta for k, meta in record.fields_get().items() if k in dct.keys()
    }
    result = {}
    for key, value in dct.items():
        if isinstance(value, dict):
            model_obj = get_model_for_read(fields_with_meta[key]["relation"], ENV)
            inner_result = transform_dictfields_to_list_of_tuples(model_obj, value, ENV)
            is_2many = fields_with_meta[key]["type"].endswith("2many")
            result[key] = list(inner_result) if is_2many else tuple(inner_result)
        else:
            result[key] = value
    return [(key, value) if value else key for key, value in result.items()]


#######################
# Pinguin ORM Wrapper #
#######################


# List of dicts from model
def get_dictlist_from_model(model, spec, **kwargs):
    """Fetch dictionary from one record according to spec.
    :param str model: The model against which to validate.
    :param tuple spec: The spec to validate.
    :param dict kwargs: Keyword arguments.
    :param list kwargs['domain']: (optional). The domain to filter on.
    :param int kwargs['offset']: (optional). The offset of the queried records.
    :param int kwargs['limit']: (optional). The limit to query.
    :param str kwargs['order']: (optional). The postgres order string.
    :param tuple kwargs['include_fields']: (optional). The extra fields.
        This parameter is not implemented on higher level code in order
        to serve as a soft ACL implementation on top of the framework's
        own ACL.
    :param tuple kwargs['exclude_fields']: (optional). The excluded fields.
    :param char kwargs['delimeter']: delimeter of nested fields.
    :param object kwargs['env']: Model's environment.
    :returns: The list of python dictionaries of the requested values.
    :rtype: list
    """
    domain = kwargs.get("domain", [])
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit")
    order = kwargs.get("order")
    include_fields = kwargs.get(
        "include_fields", ()
    )  # Not actually implemented on higher level (ACL!)
    exclude_fields = kwargs.get("exclude_fields", ())
    delim = kwargs.get("delimeter", "/")
    ENV = kwargs.get("env", False)

    model_obj = get_model_for_read(model, ENV)

    records = model_obj.sudo().search(domain, offset=offset, limit=limit, order=order)

    # Do some optimization for subfields
    _prefetch = {}
    for field in spec:
        if isinstance(field, str):
            continue
        _fld = records._fields[field[0]]
        if _fld.relational:
            _prefetch[_fld.comodel] = records.mapped(field[0]).ids

    for mod, ids in _prefetch.items():
        get_model_for_read(mod, ENV).browse(ids).read()

    result = []
    for record in records:
        result += [
            get_dict_from_record(
                record, spec, include_fields, exclude_fields, ENV, delim
            )
        ]

    return result


# Get a model with special context
def get_model_for_read(model, ENV=False):
    """Fetch a model object from the environment optimized for read.
    Postgres serialization levels are changed to allow parallel read queries.
    To increase the overall efficiency, as it is unlikely this API will be used
    as a mass transactional interface. Rather we assume sequential and structured
    integration workflows.
    :param str model: The model to retrieve from the environment.
    :param object env: Environment
    :returns: the framework model if exist, otherwise raises.
    :rtype: odoo.models.Model
    :raise: werkzeug.exceptions.HTTPException if the model not found in env.
    """
    if ENV:
        return ENV[model]
    cr, uid = request.cr, request.session.uid
    test_mode = request.registry.test_cr
    if not test_mode:
        # Permit parallel query execution on read
        # Contrary to ISOLATION_LEVEL_SERIALIZABLE as per Odoo Standard
        cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    try:
        return request.env(cr, uid)[model]
    except KeyError:
        err = list(CODE__obj_not_found)
        err[2] = 'The "%s" model is not available on this instance.' % model
        raise werkzeug.exceptions.HTTPException(response=error_response(*err))


# Python > 3.5
# def get_dict_from_record(record, spec: tuple, include_fields: tuple, exclude_fields: tuple):

# Extract nested values from a record
def get_dict_from_record(
    record, spec, include_fields, exclude_fields, ENV=False, delim="/"
):
    """Generates nested python dict representing one record.
    Going down to the record level, as the framework does not support nested
    data queries natively as they are typical for a REST API.
    :param odoo.models.Model record: The singleton record to load.
    :param tuple spec: The field spec to load.
    :param tuple include_fields: The extra fields.
    :param tuple exclude_fields: The excluded fields.
    :returns: The python dictionary representing the record according to the field spec.
    :rtype collections.OrderedDict
    """
    map(validate_extra_field, include_fields + exclude_fields)
    result = collections.OrderedDict([])
    _spec = [fld for fld in spec if fld not in exclude_fields] + list(include_fields)
    if list(filter(lambda x: isinstance(x, six.string_types) and delim in x, _spec)):
        _spec = transform_dictfields_to_list_of_tuples(
            record, transform_strfields_to_dict(_spec, delim), ENV
        )
    validate_spec(record, _spec)

    for field in _spec:

        if isinstance(field, tuple):
            # It's a 2many (or a 2one specified as a list)
            if isinstance(field[1], list):
                result[field[0]] = []
                for rec in record[field[0]]:
                    result[field[0]] += [
                        get_dict_from_record(rec, field[1], (), (), ENV, delim)
                    ]
            # It's a 2one
            if isinstance(field[1], tuple):
                result[field[0]] = get_dict_from_record(
                    record[field[0]], field[1], (), (), ENV, delim
                )
        # Normal field, or unspecified relational
        elif isinstance(field, six.string_types):
            if not hasattr(record, field):
                raise odoo.exceptions.ValidationError(
                    odoo._('The model "%s" has no such field: "%s".')
                    % (record._name, field)
                )

            # result[field] = getattr(record, field)
            if isinstance(record[field], datetime.date):
                value = record[field].strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = record[field]

            result[field] = value
            fld = record._fields[field]
            if fld.relational:
                if fld.type.endswith("2one"):
                    result[field] = value.id
                elif fld.type.endswith("2many"):
                    result[field] = value.ids
            elif (value is False or value is None) and fld.type != "boolean":
                # string field cannot be false in response json
                result[field] = ""
    return result
