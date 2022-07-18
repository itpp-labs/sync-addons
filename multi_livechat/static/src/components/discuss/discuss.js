/** @odoo-module **/

import { Discuss } from "@mail/components/discuss/discuss";

import { patch } from "web.utils";

const components = { Discuss };

patch(
    components.Discuss.prototype,
    "multi_livechat/static/src/components/discuss/discuss.js",
    {
        // --------------------------------------------------------------------------
        // Public
        // --------------------------------------------------------------------------

        /**
         * @override
         */
        mobileNavbarTabs_TODO(...args) {
            // TODO
            return [
                ...this._super(...args),
                {
                    icon: "fa fa-comments",
                    id: "livechat",
                    label: this.env._t("Livechat"),
                },
            ];
        },
    }
);
