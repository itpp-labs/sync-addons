/** @odoo-module **/

import { clear } from "@mail/model/model_field_command";
import { one } from "@mail/model/model_field";
import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "Thread",
    fields: {
        hasInviteFeature: {
            compute() {
                if (
                    this.channel &&
                    this.channel.channel_type.startsWith("multi_livechat_")
                ) {
                    return true;
                }
                return this._super();
            },
        },
        hasMemberListFeature: {
            compute() {
                if (
                    this.channel &&
                    this.channel.channel_type.startsWith("multi_livechat_")
                ) {
                    return true;
                }
                return this._super();
            },
        },
        isChatChannel: {
            compute() {
                if (
                    this.channel &&
                    this.channel.channel_type.startsWith("multi_livechat_")
                ) {
                    return true;
                }
                return this._super();
            },
        },
        /**
         * If set, current thread is a livechat.
         */
        messagingAsPinnedMLChat: one("Messaging", {
            compute() {
                if (
                    !this.messaging ||
                    !this.channel ||
                    !this.channel.channel_type.startsWith("multi_livechat_") ||
                    !this.isPinned
                ) {
                    return clear();
                }
                return this.messaging;
            },
            inverse: "pinnedMLChats",
        }),
    },
});
