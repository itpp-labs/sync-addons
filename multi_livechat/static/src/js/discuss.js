odoo.define("multi_livechat.Discuss", function (require) {
    "use strict";

    var core = require("web.core");
    var QWeb = core.qweb;
    var Discuss = require("mail.Discuss");

    Discuss.include({
        events: _.extend({}, Discuss.prototype.events, {
            "click .o_mail_open_multi_livechat_channels": "_onMultiLivechatTitleClick",
        }),

        init: function (parent, action, options) {
            this._super.apply(this, arguments);
            this.options.getNonMultiLivechatChannels = this._getNonMultiLivechatChannels.bind(
                this
            );
            this.options.getMultiLivechatChannels = this._getMultiLivechatChannels.bind(
                this
            );
            this.options.getGroupedMultiLivechatChannels = this._getGroupedMultiLivechatChannels.bind(
                this
            );
            this.options.getMultiLivechatData = this._getMultiLivechatData.bind(this);
        },

        _onMultiLivechatTitleClick: function (ev) {
            this.do_action(
                {
                    name: ev.currentTarget.dataset.multiLivechatTitle,
                    type: "ir.actions.act_window",
                    res_model: "mail.channel",
                    views: [
                        [false, "kanban"],
                        [false, "form"],
                    ],
                    domain: [
                        [
                            "channel_type",
                            "=",
                            ev.currentTarget.dataset.multiLivechatTitle,
                        ],
                    ],
                },
                {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                }
            );
        },

        _getGroupedMultiLivechatChannels: function (channels) {
            var groups = {};
            var multiLivechatData = this._getMultiLivechatData();
            var allChats = channels;
            _.each(multiLivechatData.channel_types, function (name, channel_type) {
                groups[channel_type] = {
                    channel_type: channel_type,
                    name: name,
                    chats: [],
                };
            });

            _.each(allChats, (chat) => {
                if (groups[chat._serverType]) {
                    groups[chat._serverType].chats.push(chat);
                }
            });

            return _.map(groups, (value) => value);
        },

        _getNonMultiLivechatChannels: function (channels) {
            return channels.filter(function (x) {
                return x._serverType.indexOf("multi_livechat_") !== 0;
            });
        },

        _getMultiLivechatChannels: function (channels) {
            return channels.filter(function (x) {
                return x._serverType.indexOf("multi_livechat_") === 0;
            });
        },

        _getMultiLivechatData: function () {
            return this.call("mail_service", "getMultiLivechatData");
        },

        // Based on Odoo 13.0
        // https://github.com/odoo/odoo/blob/3097e0b977ddbaa9efc4c3e60399d169dee45604/addons/mail/static/src/js/discuss.js#L779-L795
        _renderSidebarChannels: function (options) {
            console.log(options);
            options.searchChannelVal = options.searchChannelVal || "";
            var channels = this.call("mail_service", "getChannels");
            var searchChannelValLowerCase = options.searchChannelVal.toLowerCase();
            channels = _.filter(channels, function (channel) {
                var channelNameLowerCase = channel.getName().toLowerCase();
                return channelNameLowerCase.indexOf(searchChannelValLowerCase) !== -1;
            });
            channels = this._sortChannels(channels);
            this.$(".o_mail_discuss_sidebar_channels").html(
                QWeb.render("mail.discuss.SidebarChannels", {
                    activeThreadID: this._thread ? this._thread.getID() : undefined,
                    channels: channels,
                    displayQuickSearch:
                        channels.length >= this.options.channelQuickSearchThreshold,
                    // This was added comparing to original method:
                    options: this.options,
                })
            );
        },
    });
});
