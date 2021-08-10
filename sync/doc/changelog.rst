`4.2.0`
-------

- **Improvement:** add eval context function `record2image`

`4.1.2`
-------

- **Improvement:** initial values do not overwrite parameter values after a module update.
- **Fix:** add exporting of text parameter values

`4.1.1`
-------

- **Fix:** For empty `links`, the property `links.odoo` must return empty recordset, not `None`

`4.1.0`
-------

- **Improvement:** add more eval context functions (`get_lang`, `url2base64`, `html2plaintext`)
- **Improvement:** add development tools (`LogExternalQuery`), add new type for `ir.logging`
- **Improvement:** move code checker above in task form to make it more visible
- **Fix:** delete `website_published` for sake of simplicity and to avoid webhooks problem on upgrading the module to v4.0.0+

`4.0.1`
-------

- **Fix:** set project as archived by default to avoid errors on installation and updating sync modules

`4.0.0`
-------

**Improvement:** remove Website module from dependencies, handle webhooks directly in Sync Studio

`3.1.2`
-------

- **Improvement:** Manager access group renamed to Administrator

`3.1.1`
-------

- **Fix:** allow getting link after setting it

`3.1.0`
-------

- **Improvement:** generate cleaner xmlid on generating XML data file
- **Improvement:** dynamically check python code for syntax errors
- **Fix:** support POST methods in http webhooks
- **Fix:** allow change field "active" for DB Triggers

`3.0.0`
-------

**Improvement:** add translatable multi-line parameters and make original params non-translatable
**Improvement:** add the possibility to fully duplicate the project

`2.1.3`
-------

- **Fix:** Export Xml: add missed field `filter_domain`, `filter_pre_domain`

`2.1.2`
-------

- **Fix:** error on adding new webhook

`2.1.1`
-------

- **Fix:** resolving name conflicts with the demo project

`2.1.0`
-------

- **Improvement:** add tokens for incoming webhooks
- **Improvement:** add helpers for one2one synchronization
- **Improvement:** show icon in app switcher in Odoo EE
- **Fix:** error on opening "Project for Unittests"
- **Fix:** Export XML: add missed fields webhook_type

`2.0.1`
-------

- **Improvement:** add the ability to get type of the given object

`2.0.0`
-------

- **Improvement:** for security sake imports are available via module code only

`1.0.0`
-------

- **Init version**
