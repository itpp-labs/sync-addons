# License MIT (https://opensource.org/licenses/MIT).

def post_load():
    # make import in post_load to avoid applying monkey patches when this
    # module is not installed
    from . import models
    from . import controllers
