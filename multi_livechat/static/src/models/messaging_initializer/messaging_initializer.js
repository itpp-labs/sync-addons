/** @odoo-module **/

import { insertAndReplace } from "@mail/model/model_field_command";
import { registerInstancePatchModel } from "@mail/model/model_core";

registerInstancePatchModel(
    "mail.messaging_initializer",
    "multi_livechat/static/src/models/messaging_initializer/messaging_initializer.js",
    {
        _initResUsersSettings(settings) {
            const data = {};
            _.each(this.messaging.discuss.getMLChatCategories(), (chat, field_name) => {
                const NAME = field_name.split("categoryMLChat_")[1];
                const display_name = (
                    NAME.charAt(0).toUpperCase() + NAME.slice(1)
                ).replace("_", " ");
                const state_key = "is_discuss_sidebar_category_" + NAME + "_open";
                data[field_name] = insertAndReplace({
                    isServerOpen: settings[state_key],
                    name: display_name,
                    serverStateKey: state_key,
                    sortComputeMethod: "last_action",
                    supportedChannelTypes: [NAME],
                });
            });

            this.messaging.discuss.update(data);
            this._super(...arguments);
        },
    }
);
