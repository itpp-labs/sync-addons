# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
import base64
import csv
import json
from io import StringIO

import yaml

from odoo import fields, models


class SyncData(models.Model):
    _name = "sync.data"
    _description = "Sync Data File"

    name = fields.Char("Technical name")
    project_id = fields.Many2one("sync.project", ondelete="cascade")
    file_name = fields.Char("File Name")
    file_content = fields.Binary("File Content")

    def csv(self, *args, **kwargs):
        """Parse CSV file from binary field."""
        if self.file_content:
            file_content = base64.b64decode(self.file_content)
            file_content = file_content.decode("utf-8")
            file_like_object = StringIO(file_content)
            reader = csv.DictReader(file_like_object, *args, **kwargs)
            return [row for row in reader]
        return []

    def json(self):
        """Parse JSON file from binary field."""
        if self.file_content:
            file_content = base64.b64decode(self.file_content)
            file_content = file_content.decode("utf-8")
            return json.loads(file_content)
        return {}

    def yaml(self):
        """Parse YAML file from binary field."""
        if self.file_content:
            file_content = base64.b64decode(self.file_content)
            file_content = file_content.decode("utf-8")
            return yaml.safe_load(file_content)
        return None
