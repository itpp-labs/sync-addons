/** @odoo-module **/

import { registerInstancePatchModel } from "@mail/model/model_core";

registerInstancePatchModel(
    "mail.messaging_notification_handler",
    "multi_livechat/static/src/models/messaging_notification_handler/messaging_notification_handler.js",
    {
        // ----------------------------------------------------------------------
        // Private
        // ----------------------------------------------------------------------

        /**
         * @override
         * @param {Object} settings
         * @param {Boolean} [settings.is_discuss_sidebar_category_livechat_open]
         */
        _handleNotificationResUsersSettings(settings) {
            _.each(this.messaging.discuss.getMLChatCategories(), (chat, field_name) => {
                const NAME = field_name.split("categoryMLChat_")[1];
                const key = "is_discuss_sidebar_category_" + NAME + "_open";
                if (key in settings) {
                    const category = "categoryMLChat_" + NAME;
                    this.messaging.discuss[category].update({
                        isServerOpen: settings[key],
                    });
                }
            });
            this._super(settings);
        },

        // TODO
        _handleNotificationChannelPartnerTypingStatus_TODO({
            channel_id,
            is_typing,
            livechat_username,
            partner_id,
            partner_name,
        }) {
            const channel = this.messaging.models[
                "mail.thread"
            ].findFromIdentifyingData({
                id: channel_id,
                model: "mail.channel",
            });
            if (!channel) {
                return;
            }
            let partnerId = partner_id;
            let partnerName = partner_name;
            if (
                this.messaging.publicPartners.some(
                    (publicPartner) => publicPartner.id === partner_id
                )
            ) {
                // Some shenanigans that this is a typing notification
                // from public partner.
                partnerId = channel.correspondent.id;
                partnerName = channel.correspondent.name;
            }
            const data = {
                channel_id,
                is_typing,
                partner_id: partnerId,
                partner_name: partnerName,
            };
            if (livechat_username) {
                // Flux specific, livechat_username is returned instead of name for livechat channels
                // Value still present for API compatibility in stable
                delete data.partner_name;
                this.models["mail.partner"].insert({
                    id: partnerId,
                    livechat_username: livechat_username,
                });
            }
            this._super(data);
        },
    }
);
