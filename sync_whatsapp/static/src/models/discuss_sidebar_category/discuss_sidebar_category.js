/** @odoo-module **/

import {
    registerFieldPatchModel,
    registerIdentifyingFieldsPatch,
} from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel("mail.discuss_sidebar_category", "sync_whatsapp", {
    discussAsMLChat_whatsapp_chatapi: one2one("mail.discuss", {
        inverse: "categoryMLChat_whatsapp_chatapi",
        readonly: true,
    }),
});

registerIdentifyingFieldsPatch(
    "mail.discuss_sidebar_category",
    "sync_whatsapp",
    (identifyingFields) => {
        identifyingFields[0].push("discussAsMLChat_whatsapp_chatapi");
    }
);
