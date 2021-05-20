odoo.define(
    "sync_telegram/static/src/mail/models/messaging_initializer/messaging_initializer.js",
    function (require) {
        "use strict";

        const {
            registerInstancePatchModel,
        } = require("mail/static/src/model/model_core.js");
        const {executeGracefully} = require("mail/static/src/utils/utils.js");

        registerInstancePatchModel(
            "mail.messaging_initializer",
            "sync_telegram/static/src/mail/models/messaging_initializer/messaging_initializer.js",
            {
                async _initChannels(initMessagingData) {
                    await this.async(() => this._super(initMessagingData));
                    const {channel_telegram = []} = initMessagingData;
                    return executeGracefully(
                        channel_telegram.map((data) => () => {
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
