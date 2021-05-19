odoo.define(
    "sync_telegram/static/src/mail/components/discuss_sidebar/discuss_sidebar.js",
    function (require) {
        "use strict";

        const components = {
            DiscussSidebar: require("mail/static/src/components/discuss_sidebar/discuss_sidebar.js"),
        };

        const {patch} = require("web.utils");

        patch(
            components.DiscussSidebar,
            "sync_telegram/static/src/mail/components/discuss_sidebar/discuss_sidebar.js",
            {
                // --------------------------------------------------------------------------
                // Public
                // --------------------------------------------------------------------------

                /**
                 * Return the list of chats that match the quick search value input.
                 *
                 * @returns {mail.thread[]}
                 */
                quickSearchOrderedAndPinnedTelegramChatList() {
                    const allOrderedAndPinnedTelegramChats = this.env.models[
                        "mail.thread"
                    ]
                        .all(
                            (thread) =>
                                thread.channel_type === "telegram" &&
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
                    if (!this.discuss.sidebarQuickSearchValue) {
                        return allOrderedAndPinnedTelegramChats;
                    }
                    const qsVal = this.discuss.sidebarQuickSearchValue.toLowerCase();
                    return allOrderedAndPinnedTelegramChats.filter((chat) => {
                        const nameVal = chat.displayName.toLowerCase();
                        return nameVal.includes(qsVal);
                    });
                },

                // --------------------------------------------------------------------------
                // Private
                // --------------------------------------------------------------------------

                /**
                 * @override
                 */
                _useStoreCompareDepth() {
                    return Object.assign(this._super(...arguments), {
                        allOrderedAndPinnedTelegramChats: 1,
                    });
                },
                /**
                 * Override to include chat channels on the sidebar.
                 *
                 * @override
                 */
                _useStoreSelector(props) {
                    return Object.assign(this._super(...arguments), {
                        allOrderedAndPinnedTelegramChats: this.quickSearchOrderedAndPinnedTelegramChatList(),
                    });
                },
            }
        );
    }
);
