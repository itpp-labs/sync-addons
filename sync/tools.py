# Copyright 2021,2024 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import ast
import base64
import functools
import json
import re

import markdown
import requests
import urllib3
import yaml

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


def extract_yaml(content, pattern, missing_message="No YAML front matter found."):
    """
    Extracts and parses YAML front matter using the given regex pattern.

    Args:
    content (str): The full content containing YAML front matter.
    pattern (str): A regular expression pattern to match YAML front matter.
    missing_message (str): An error message to raise if no YAML is found.

    Returns:
    dict: A dictionary containing the parsed YAML.

    Raises:
    ValueError: If no YAML is found or if there is a parsing error.
    """
    # Match the content against the pattern
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        raise ValueError(missing_message)

    # Extract the YAML string
    yaml_content = match.group(1)

    # Parse the YAML
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML: {exc}") from exc


def extract_yaml_from_markdown(markdown_content):
    """
    Extracts and parses the YAML front matter from the given Markdown file content.

    Args:
    markdown_content (str): The content of the Markdown file as a string.

    Returns:
    dict: A dictionary containing the parsed YAML.

    Raises:
    ValueError: If no YAML front matter is found or if there is a parsing error.
    """
    # Regular expression to find YAML delimited by ---
    markdown_pattern = r"^---\s*\n(.*?)\n---"
    return extract_yaml(markdown_content, markdown_pattern)


def extract_yaml_from_python(python_content):
    """
    Extracts and parses the YAML front matter from the given Python file content.

    Args:
    python_content (str): The content of the Python file as a string.

    Returns:
    dict: A dictionary containing the parsed YAML.

    Raises:
    ValueError: If no YAML front matter is found or if there is a parsing error.
    """
    # Regular expression to find YAML enclosed in triple quotes (""")
    python_pattern = r'^"""(.*?)"""'
    return extract_yaml(python_content, python_pattern)


def has_function_defined(python_code, function_name):
    """
    Check if a function with a specific name is defined in the given Python code.

    Args:
    python_code (str): The Python code to analyze.
    function_name (str): The name of the function to look for.

    Returns:
    bool: True if the function is defined, False otherwise.
    """
    # Parse the code into an abstract syntax tree (AST)
    try:
        tree = ast.parse(python_code)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code provided: {exc}") from exc

    # Traverse the tree to find function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return True

    return False


def convert_python_front_matter_to_comment(file_content):
    """
    Converts front matter in triple quotes at the top of a Python file into commented lines.

    Args:
    file_content (str): The content of the Python file.

    Returns:
    str: The modified file content with the front matter commented out.
    """
    # Regex to match the front matter enclosed in triple quotes
    pattern = r'^("""[\s\S]+?""")'

    # Function to add a hash in front of each line within the triple quotes
    def comment(match):
        commented = "\n".join(
            "# " + line if line.strip() != "" else "#"
            for line in match.group(1).split("\n")
        )
        return commented

    # Replace the front matter with its commented version
    modified_content = re.sub(pattern, comment, file_content, count=1)

    return modified_content


def add_items(container, *args, **kwargs):
    """
    Adds items to the container. Handles functions, dictionaries, and positional arguments, adding them appropriately.
    Also adds key-value pairs from keyword arguments directly to the container.
    """
    for item in args:
        if callable(item):
            container[item.__name__] = item
        elif isinstance(item, dict) and not isinstance(item, AttrDict):
            container.update(item)
        else:
            raise Exception(
                f"The container received a non-callable positional argument of type "
                f"'{type(item).__name__}', which lacks an explicit name. "
                f"Please pass a callable, a dictionary, or provide a key-value pair using keyword arguments."
            )
    container.update(kwargs)


class AttrDict(dict):
    """
    A dictionary that allows for attribute-style access. Automatically updates both keys and attributes.
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__()
        add_items(self, *args, **kwargs)
        self.__dict__ = self
