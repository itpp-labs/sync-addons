/** @odoo-module **/

import { clear } from "@mail/model/model_field_command";
import { one } from "@mail/model/model_field";
import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "DiscussSidebarCategory",
    fields: {
        categoryItemsOrderedByLastAction: {
            compute() {
                if (this.discussAsMLChat_echo_demo) {
                    return this.categoryItems;
                }
                return this._super();
            },
        },
        discussAsMLChat_echo_demo: one("Discuss", {
            identifying: true,
            inverse: "categoryMLChat_echo_demo",
        }),
        isServerOpen: {
            compute() {
                // There is no server state for non-users (guests)
                if (!this.messaging.currentUser) {
                    return clear();
                }
                if (!this.messaging.currentUser.res_users_settings_id) {
                    return clear();
                }
                if (this.discussAsMLChat_echo_demo) {
                    return this.messaging.currentUser.res_users_settings_id
                        .is_discuss_sidebar_category_echo_demo_open;
                }
                return this._super();
            },
        },
        name: {
            compute() {
                if (this.discussAsMLChat_echo_demo) {
                    return this.env._t("Echo Chat (demo)");
                }
                return this._super();
            },
        },
        orderedCategoryItems: {
            compute() {
                if (this.discussAsMLChat_echo_demo) {
                    return this.categoryItemsOrderedByLastAction;
                }
                return this._super();
            },
        },
        serverStateKey: {
            compute() {
                if (this.discussAsMLChat_echo_demo) {
                    return "is_discuss_sidebar_category_echo_demo_open";
                }
                return this._super();
            },
        },
        supportedChannelTypes: {
            compute() {
                if (this.discussAsMLChat_echo_demo) {
                    return ["echo_demo"];
                }
                return this._super();
            },
        },
    },
});
