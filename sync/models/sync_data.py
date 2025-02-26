# Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev>
import base64
import csv
import json
from io import StringIO

import yaml

from odoo import api, fields, models


class SyncData(models.Model):
    _name = "sync.data"
    _description = "Sync Data File"

    name = fields.Char("Technical name")
    project_id = fields.Many2one("sync.project", ondelete="cascade")
    file_name = fields.Char("File Name")
    file_content = fields.Binary("File Content")
    text = fields.Text("Decoded Text", compute="_compute_text")

    @api.depends("file_content")
    def _compute_text(self):
        for record in self:
            if record.file_content:
                decoded_content = base64.b64decode(record.file_content)
                record.text = decoded_content.decode("utf-8")
            else:
                record.text = False

    def csv(self, *args, **kwargs):
        """Parse CSV file from binary field."""
        if self.file_content:
            file_like_object = StringIO(self.text)
            reader = csv.DictReader(file_like_object, *args, **kwargs)
            return [row for row in reader]
        return []

    def json(self):
        """Parse JSON file from binary field."""
        if self.file_content:
            return json.loads(self.text)
        return {}

    def yaml(self):
        """Parse YAML file from binary field."""
        if self.file_content:
            return yaml.safe_load(self.text)
        return None
