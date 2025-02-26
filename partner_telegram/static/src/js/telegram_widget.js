/** @odoo-module **/
/** Copyright 2024 Ivan Yelizariev <https://twitter.com/yelizariev> **/

import { EmailField } from "@web/views/fields/email/email_field";
import { registry } from "@web/core/registry";

class TelegramField extends EmailField {}

TelegramField.template = "partner_contact.TelegramField";

class FormTelegramField extends TelegramField {}
FormTelegramField.template = "partner_contact.FormTelegramField";

registry.category("fields").add("telegram", TelegramField);
registry.category("fields").add("form.telegram", FormTelegramField);
