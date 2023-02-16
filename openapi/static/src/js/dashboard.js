/*
Copyright 2018-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
*/
odoo.define("openapi.dashboard", function (require) {
    var Widget = require("web.Widget");
    var dashboard = require("web_settings_dashboard");

    var DashboardOpenAPI = Widget.extend({
        template: "DashboardOpenAPI",

        events: {
            //     'click .o_pay_subscription': 'on_pay_subscription',
            "click .o_openapi_create": "on_openapi_create",
            "click .o_openapi_namespace": "on_namespace_clicked",
        },

        init: function (parent, data) {
            this.data = data;
            this.parent = parent;
            return this._super.apply(this, arguments);
        },

        // On_pay_subscription: function(){

        // },

        on_openapi_create: function () {
            this.do_action({
                type: "ir.actions.act_window",
                res_model: "openapi.namespace",
                views: [[false, "form"]],
                target: "new",
            });
        },

        on_namespace_clicked: function (e) {
            var self = this;
            e.preventDefault();
            var namespace_id = $(e.currentTarget).data("namespace-id");
            var action = {
                type: "ir.actions.act_window",
                view_type: "form",
                view_mode: "form",
                res_model: "openapi.namespace",
                res_id: namespace_id,
                views: [[false, "form"]],
                target: "new",
            };
            this.do_action(action, {
                on_reverse_breadcrumb: function () {
                    return self.reload();
                },
            });
        },
    });

    dashboard.Dashboard.include({
        init: function (parent, data) {
            var ret = this._super(parent, data);
            this.all_dashboards.push("openapi");
            return ret;
        },
        load_openapi: function (data) {
            if (data.openapi_not_allowed === true) {
                return $.when();
            }
            this.$(".o_web_settings_dashboard_openapi").parent().show();
            return new DashboardOpenAPI(this, data.openapi).replace(
                this.$(".o_web_settings_dashboard_openapi")
            );
        },
    });
});
