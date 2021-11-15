odoo.define("multi_livechat.Manager", function (require) {
    "use strict";

    var MailManager = require("mail.Manager");

    MailManager.include({
        _updateInternalStateFromServer: function (result) {
            this._multi_livechat = result.multi_livechat;
            return this._super.apply(this, arguments);
        },

        getMultiLivechatData: function () {
            return this._multi_livechat;
        },
    });
});
