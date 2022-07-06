/** @odoo-module **/

import { registerFieldPatchModel } from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel(
    "mail.discuss",
    "sync_telegram/static/src/models/discuss/discuss.js",
    {
        categoryMLChat_telegram: one2one("mail.discuss_sidebar_category", {
            inverse: "discussAsMLChat_telegram",
            isCausal: true,
        }),
    }
);
