odoo.define(
    "multi_livechat/static/src/mail/models/messaging_initializer/messaging_initializer.js",
    function (require) {


        const ODOO_CHANNEL_GROUPS = [
            "channel_channel",
            "channel_direct_message",
            "channel_private_group",
            "channel_livechat",
        ];

        const {
            registerInstancePatchModel,
        } = require("mail/static/src/model/model_core.js");
        const { executeGracefully } = require("mail/static/src/utils/utils.js");

        registerInstancePatchModel(
            "mail.messaging_initializer",
            "multi_livechat/static/src/mail/models/messaging_initializer/messaging_initializer.js",
            {
                async _init(data) {
                    await this.async(() => this._super(data));
                    // TODO: find a better way
                    this.env.messaging.multi_livechat = data.multi_livechat;
                },
                async _initChannels(initMessagingData) {
                    await this.async(() => this._super(initMessagingData));
                    let channel_list = [];
                    for (const key in initMessagingData) {
                        const startsWith = key.lastIndexOf("multi_livechat_") === 0;
                        if (startsWith && !(key in ODOO_CHANNEL_GROUPS)) {
                            channel_list = channel_list.concat(initMessagingData[key]);
                        }
                    }
                    // TODO: multi_livechat_types: channel_type -> Channel Name
                    return executeGracefully(
                        channel_list.map((data) => () => {
                            const channel = this.env.models["mail.thread"].insert(
                                this.env.models["mail.thread"].convertData(data)
                            );
                            if (!channel.isPinned) {
                                channel.pin();
                            }
                        })
                    );
                },
            }
        );
    }
);
