/** @odoo-module **/
/** Copyright 2024-2025 Ivan Yelizariev <https://twitter.com/yelizariev> **/

import { EmailField } from "@web/views/fields/email/email_field";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

class TelegramField extends EmailField {}

TelegramField.template = "partner_contact.TelegramField";

export const telegramField = {
    component: TelegramField,
    displayName: _t("Telegram"),
    supportedTypes: ["char"],
    extractProps: ({ attrs }) => ({
        placeholder: attrs.placeholder,
    }),
};

registry.category("fields").add("telegram", telegramField);

class FormTelegramField extends TelegramField {}
FormTelegramField.template = "partner_contact.FormTelegramField";

export const formTelegramField = {
    ...telegramField,
    component: FormTelegramField,
};

registry.category("fields").add("form.telegram", formTelegramField);
