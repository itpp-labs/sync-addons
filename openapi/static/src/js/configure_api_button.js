/*
Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
*/
odoo.define('openapi.configure_API', function (require) {

    var ListView = require('web.ListView');
    var Model = require('web.DataModel');
    var IrModel = new Model('ir.model');

    function openapi_add_configure_action () {
        var self = this;
        IrModel.call(
            'search', [['|', ['name', '=', 'openapi.namespace'], ['model', '=', 'openapi.namespace']]]
        ).then(function(ids) {
            var context = {
                'default_model': self.model,
                'default_model_id': ids[0],
            };
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: "openapi.access",
                views: [[false, 'form']],
                target: 'new',
                context: context,
            });
        });
    }

    ListView.include({
        render_buttons: function() {
            this._super.apply(this, arguments);
            this.$buttons.on('click', '.o_button_openapi_add_configure', openapi_add_configure_action.bind(this));
        }
    });

    // it may be needed
    // var KanbanView = require('web_kanban.KanbanView');
    // KanbanView.include({
    //     render_buttons: function() {
    //         this._super.apply(this, arguments); // Sets this.$buttons
    //         this.$buttons.on('click', '.o_button_openapi_add_configure', openapi_add_configure_action.bind(this));
    //     },
    // });
});
