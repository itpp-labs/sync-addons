# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from . import controllers
from . import models

def post_load():
    from .controllers import apijsonrequest
