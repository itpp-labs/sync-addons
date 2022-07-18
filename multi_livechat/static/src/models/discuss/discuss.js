/** @odoo-module **/

import { registerInstancePatchModel } from "@mail/model/model_core";

registerInstancePatchModel(
    "mail.discuss",
    "multi_livechat/static/src/models/discuss/discuss.js",
    {
        /**
         * @override
         */
        onInputQuickSearch_TODO(value) {
            if (!this.sidebarQuickSearchValue) {
                // TODO
                // this.categoryLivechat.open();
            }
            return this._super(value);
        },
        getMLChatCategories() {
            // CategoryMLChat_NAME -> field
            const res = {};
            _.each(this.__values, (value, key) => {
                if (key.startsWith("categoryMLChat_")) {
                    res[key] = value;
                }
            });
            return res;
        },
    }
);
