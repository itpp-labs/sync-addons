/** @odoo-module **/

import { registerFieldPatchModel } from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel(
    "mail.discuss",
    "sync_whatsapp/static/src/models/discuss/discuss.js",
    {
        categoryMLChat_whatsapp_chatapi: one2one("mail.discuss_sidebar_category", {
            inverse: "discussAsMLChat_whatsapp_chatapi",
            isCausal: true,
        }),
    }
);
