# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import functools

import requests

from .models.ir_logging import LOG_ERROR


class LogExternalQuery(object):
    """Adds logs before and after external query.
    Can be used for eval context method.
    Example:

        @LogExternalQuery("Viber->send_messages", eval_context)
        def send_messages(to, messages):
            return viber.send_messages(to, messages)
    """

    def __init__(self, target_name, eval_context):
        self.target_name = target_name
        self.log = eval_context["log"]
        self.log_transmission = eval_context["log_transmission"]

    def __call__(self, func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            self.log_transmission(
                self.target_name,
                "*%s, **%s"
                % (
                    args,
                    kwargs,
                ),
            )
            try:
                res = func(*args, **kwargs)
            except Exception as err:
                self.log(
                    str(err), name=self.target_name, log_type="data_in", level=LOG_ERROR
                )
                raise
            self.log("RESULT: %s" % res, name=self.target_name, log_type="data_in")
            return res

        return wrap


def url2bin(url):
    if not url:
        return None
    r = requests.get(url, timeout=42)
    return r.content


# E.g. to download file and save into in an attachment or Binary field
def url2base64(url):
    content = url2bin(url)
    if not bin:
        return None
    return base64.b64encode(content)
