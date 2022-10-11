/** @odoo-module **/

import {
    registerFieldPatchModel,
    registerIdentifyingFieldsPatch,
} from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel("mail.discuss_sidebar_category", "sync_viber", {
    discussAsMLChat_viber: one2one("mail.discuss", {
        inverse: "categoryMLChat_viber",
        readonly: true,
    }),
});

registerIdentifyingFieldsPatch(
    "mail.discuss_sidebar_category",
    "sync_viber",
    (identifyingFields) => {
        identifyingFields[0].push("discussAsMLChat_viber");
    }
);
