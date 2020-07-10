# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
#
# Code of this file is based on odoo/tools/safe_eval.py
# License notes from there:
#
#     Part of Odoo. See LICENSE file for full copyright and licensing details.
#     Module partially ripped from/inspired by several different sources:
#      - http://code.activestate.com/recipes/286134/
#      - safe_eval in lp:~xrg/openobject-server/optimize-5.0
#      - safe_eval in tryton http://hg.tryton.org/hgwebdir.cgi/trytond/rev/bbb5f73319ad

# pylint: disable=eval-referenced

import logging
import sys
from opcode import opmap
from types import CodeType

import werkzeug
from psycopg2 import OperationalError

import odoo
from odoo.tools import pycompat
from odoo.tools.misc import ustr
from odoo.tools.safe_eval import _BUILTINS, _SAFE_OPCODES, test_expr

_logger = logging.getLogger(__name__)

_SAFE_OPCODES = _SAFE_OPCODES.union(
    {
        opmap[x]
        for x in [
            "IMPORT_NAME",
            "IMPORT_FROM",
            "LOAD_DEREF",
            "STORE_DEREF",
            "MAKE_CLOSURE",  # python 3.5 only. See https://python.readthedocs.io/en/stable/whatsnew/3.6.html
            "BUILD_TUPLE_UNPACK_WITH_CALL",  # python 3.6
            "LOAD_CLOSURE",
        ]
        if opmap.get(x)
    }
)

unsafe_eval = eval

_BUILTINS["__import__"] = __import__


# The code below differs from origin by lint changes only
def safe_eval_extra(
    expr,
    globals_dict=None,
    locals_dict=None,
    mode="eval",
    nocopy=False,
    locals_builtins=False,
):
    """safe_eval(expression[, globals[, locals[, mode[, nocopy]]]]) -> result

    System-restricted Python expression evaluation

    Evaluates a string that contains an expression that mostly
    uses Python constants, arithmetic expressions and the
    objects directly provided in context.

    This can be used to e.g. evaluate
    an OpenERP domain expression from an untrusted source.

    :throws TypeError: If the expression provided is a code object
    :throws SyntaxError: If the expression provided is not valid Python
    :throws NameError: If the expression provided accesses forbidden names
    :throws ValueError: If the expression provided uses forbidden bytecode
    """
    if type(expr) is CodeType:
        raise TypeError("safe_eval does not allow direct evaluation of code objects.")

    # prevent altering the globals/locals from within the sandbox
    # by taking a copy.
    if not nocopy:
        # isinstance() does not work below, we want *exactly* the dict class
        if (globals_dict is not None and type(globals_dict) is not dict) or (
            locals_dict is not None and type(locals_dict) is not dict
        ):
            _logger.warning(
                "Looks like you are trying to pass a dynamic environment, "
                "you should probably pass nocopy=True to safe_eval()."
            )
        if globals_dict is not None:
            globals_dict = dict(globals_dict)
        if locals_dict is not None:
            locals_dict = dict(locals_dict)

    if globals_dict is None:
        globals_dict = {}

    globals_dict["__builtins__"] = _BUILTINS
    if locals_builtins:
        if locals_dict is None:
            locals_dict = {}
        locals_dict.update(_BUILTINS)
    c = test_expr(expr, _SAFE_OPCODES, mode=mode)
    try:
        return unsafe_eval(c, globals_dict, locals_dict)
    except odoo.exceptions.except_orm:
        raise
    except odoo.exceptions.Warning:
        raise
    except odoo.exceptions.RedirectWarning:
        raise
    except odoo.exceptions.AccessDenied:
        raise
    except odoo.exceptions.AccessError:
        raise
    except werkzeug.exceptions.HTTPException:
        raise
    except odoo.http.AuthenticationError:
        raise
    except OperationalError:
        # Do not hide PostgreSQL low-level exceptions, to let the auto-replay
        # of serialized transactions work its magic
        raise
    except odoo.exceptions.MissingError:
        raise
    except Exception as e:
        exc_info = sys.exc_info()
        pycompat.reraise(
            ValueError,
            ValueError(
                '{}: "{}" while evaluating\n{!r}'.format(ustr(type(e)), ustr(e), expr)
            ),
            exc_info[2],
        )


def test_python_expr_extra(expr, mode="eval"):
    try:
        test_expr(expr, _SAFE_OPCODES, mode=mode)
    except (SyntaxError, TypeError, ValueError) as err:
        if len(err.args) >= 2 and len(err.args[1]) >= 4:
            error = {
                "message": err.args[0],
                "filename": err.args[1][0],
                "lineno": err.args[1][1],
                "offset": err.args[1][2],
                "error_line": err.args[1][3],
            }
            msg = "%s : %s at line %d\n%s" % (
                type(err).__name__,
                error["message"],
                error["lineno"],
                error["error_line"],
            )
        else:
            msg = ustr(err)
        return msg
    return False
