# Copyright 2021,2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import base64
import functools
import json
import re

import markdown
import requests
import urllib3

from odoo.exceptions import UserError
from odoo.tools.translate import _

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


def compile_markdown_to_html(markdown_content):
    markdown_content = remove_front_matter(markdown_content)

    html = markdown.markdown(markdown_content)

    return html


def remove_front_matter(markdown_content):
    # Find the front matter and remove it from the content
    front_matter_match = re.match(r"---\n.*?\n---\n", markdown_content, re.DOTALL)
    if front_matter_match:
        return markdown_content[front_matter_match.end() :]
    else:
        return markdown_content


def fetch_gist_data(gist_page):
    # https://gist.github.com/yelizariev/e0585a0817c4d87b65b8a3d945da7ca2
    # [0]   [1]     [2]          [3]                 [4]
    path_parts = gist_page.split("/")
    try:
        gist_code = path_parts[4]
    except IndexError as err:
        raise UserError(_("Not a valid gist url %s"), gist_page) from err

    # Construct the URL for the Gist API endpoint
    url = f"https://api.github.com/gists/{gist_code}"

    # TODO: support GITHUB_TOKEN
    headers = {
        # "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Create a connection pool manager
    http = urllib3.PoolManager()

    # Make the GET request to fetch the Gist information
    response = http.request("GET", url, headers=headers)
    if response.status != 200:
        raise Exception(f"Failed to fetch Gist data. Status code: {response.status}")

    # Get the Gist content from the response
    gist_content = json.loads(response.data.decode("utf-8"))

    return gist_content
