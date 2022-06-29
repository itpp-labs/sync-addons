odoo.define(
    "multi_livechat/static/src/mail/components/discuss_sidebar/discuss_sidebar.js",
    function (require) {
        const ODOO_CHANNEL_TYPES = ["chat", "channel", "livechat"];

        const components = {
            DiscussSidebar: require("mail/static/src/components/discuss_sidebar/discuss_sidebar.js"),
        };

        const { patch } = require("web.utils");

        patch(
            components.DiscussSidebar,
            "multi_livechat/static/src/components/discuss_sidebar/discuss_sidebar.js",
            {
                // --------------------------------------------------------------------------
                // Public
                // --------------------------------------------------------------------------

                /**
                 * Return the list of chats that match the quick search value input.
                 *
                 * @returns {mail.thread[]}
                 */
                getMultiLivechatGroups() {
                    let allChats = this.env.models["mail.thread"]
                        .all(
                            (thread) =>
                                !(thread.channel_type in ODOO_CHANNEL_TYPES) &&
                                thread.isPinned &&
                                thread.model === "mail.channel"
                        )
                        .sort((c1, c2) => {
                            // Sort by: last message id (desc), id (desc)
                            if (c1.lastMessage && c2.lastMessage) {
                                return c2.lastMessage.id - c1.lastMessage.id;
                            }
                            // A channel without a last message is assumed to be a new
                            // channel just created with the intent of posting a new
                            // message on it, in which case it should be moved up.
                            if (!c1.lastMessage) {
                                return -1;
                            }
                            if (!c2.lastMessage) {
                                return 1;
                            }
                            return c2.id - c1.id;
                        });
                    let qsVal = this.discuss.sidebarQuickSearchValue;
                    if (qsVal) {
                        qsVal = qsVal.toLowerCase();
                        allChats = allChats.filter((chat) => {
                            const nameVal = chat.displayName.toLowerCase();
                            return nameVal.includes(qsVal);
                        });
                    }
                    const groups = {};
                    _.each(this.env.messaging.multi_livechat.channel_types, function (
                        name,
                        channel_type
                    ) {
                        groups[channel_type] = {
                            channel_type: channel_type,
                            name: name,
                            chats: [],
                        };
                    });

                    _.each(allChats, (chat) => {
                        if (groups[chat.channel_type]) {
                            groups[chat.channel_type].chats.push(chat);
                        }
                    });

                    return _.map(groups, (value) => value);
                },

                // --------------------------------------------------------------------------
                // Private
                // --------------------------------------------------------------------------

                /**
                 * @override
                 */
                _useStoreCompareDepth() {
                    return Object.assign(this._super(...arguments), {
                        multiLivechatGroups: 2,
                    });
                },
                /**
                 * Override to include chat channels on the sidebar.
                 *
                 * @override
                 */
                _useStoreSelector(props) {
                    return Object.assign(this._super(...arguments), {
                        multiLivechatGroups: this.getMultiLivechatGroups(),
                    });
                },
                // --------------------------------------------------------------------------
                // Handlers
                // --------------------------------------------------------------------------
                _onClickLiveChatGroupTitle(channel_type) {
                    return this.env.bus.trigger("do-action", {
                        action: {
                            name: this.env._t("Channels"),
                            type: "ir.actions.act_window",
                            res_model: "mail.channel",
                            views: [
                                [false, "kanban"],
                                [false, "form"],
                            ],
                            domain: [["channel_type", "=", channel_type]],
                        },
                    });
                },
            }
        );
    }
);
