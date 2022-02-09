# Remember to bump the module version every time you make a change!

{
    "name": "Record Mapping for Sync Studio",
    "summary": "Adds a more intuitive interface for managing manual record mappings between Odoo and external systems.",
    "version": "14.0.1.0.0",
    "category": "Extra Tools",
    "author": "Butopea, " "Mohammad Tomaraei",
    "website": "https://butopea.com",
    "license": "AGPL-3",
    "depends": ["base", "sync"],
    "qweb": [
      "views/debug.xml"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sync_project_views.xml",
        "views/assets.xml",
        "wizard/sync_record_mapping_wizard.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
