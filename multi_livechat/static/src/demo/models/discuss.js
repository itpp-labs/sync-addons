/** @odoo-module **/

import { one } from "@mail/model/model_field";
import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "Discuss",
    fields: {
        categoryMLChat_echo_demo: one("DiscussSidebarCategory", {
            default: {},
            inverse: "discussAsMLChat_echo_demo",
        }),
    },
});
