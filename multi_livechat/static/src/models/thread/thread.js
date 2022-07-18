/** @odoo-module **/

import { registerInstancePatchModel } from "@mail/model/model_core";

registerInstancePatchModel(
    "mail.thread",
    "multi_livechat/static/src/models/thread/thread.js",
    {
        _computeHasInviteFeature() {
            if (this.channel_type && this.channel_type.startsWith("multi_livechat_")) {
                return true;
            }
            return this._super();
        },
        /**
         * @override
         */
        _computeHasMemberListFeature() {
            if (this.channel_type && this.channel_type.startsWith("multi_livechat_")) {
                return true;
            }
            return this._super();
        },
        /**
         * @override
         */
        _computeIsChatChannel() {
            return (
                (this.channel_type &&
                    this.channel_type.startsWith("multi_livechat_")) ||
                this._super()
            );
        },
        /**
         * @override
         */
        _getDiscussSidebarCategory() {
            if (this.channel_type && this.channel_type.startsWith("multi_livechat_")) {
                const NAME = this.channel_type.split("multi_livechat_")[1];
                return this.messaging.discuss["categoryMLChat_" + NAME];
            }
            return this._super();
        },
    }
);
