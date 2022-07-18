/** @odoo-module **/

import {
    registerFieldPatchModel,
    registerIdentifyingFieldsPatch,
} from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel("mail.discuss_sidebar_category", "sync_telegram", {
    discussAsMLChat_telegram: one2one("mail.discuss", {
        inverse: "categoryMLChat_telegram",
        readonly: true,
    }),
});

registerIdentifyingFieldsPatch(
    "mail.discuss_sidebar_category",
    "sync_telegram",
    (identifyingFields) => {
        identifyingFields[0].push("discussAsMLChat_telegram");
    }
);
