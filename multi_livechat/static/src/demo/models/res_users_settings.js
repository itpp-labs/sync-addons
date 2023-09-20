/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr } from '@mail/model/model_field';

/**
 * Mirrors the fields of the python model res.users.settings.
 */
registerPatch({
    name: 'res.users.settings',
    fields: {
        is_discuss_sidebar_category_line_open: attr({
            default: true,
        }),
    },
});
