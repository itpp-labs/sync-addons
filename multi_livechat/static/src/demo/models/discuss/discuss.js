/** @odoo-module **/

import { registerFieldPatchModel } from "@mail/model/model_core";
import { one2one } from "@mail/model/model_field";

registerFieldPatchModel(
    "mail.discuss",
    "multi_livechat/static/src/models/discuss/discuss.js",
    {
        categoryMLChat_echo_demo: one2one("mail.discuss_sidebar_category", {
            inverse: "discussAsMLChat_echo_demo",
            isCausal: true,
        }),
    }
);
