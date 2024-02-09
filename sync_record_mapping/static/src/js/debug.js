odoo.define('sync_record_mapping.DebugManager.Backend', function (require) {
"use strict";

var core = require('web.core');
var DebugManager = require('web.DebugManager.Backend');

var _t = core._t;
/**
 * adds a new method available for the debug manager, called by the "Manage Record Mappings" button.
 *
 */
DebugManager.include({
    getRecordMappings: function () {
        var selectedIDs = this._controller.getSelectedIds();
        if (!selectedIDs.length) {
            console.warn(_t("At least one record must be selected to manage record mappings."));
            return;
        }
        this.do_action({
            type: 'ir.actions.act_window',
            name: _t('Manage Record Mappings'),
            res_model: 'sync.record.mapping.wizard',
            views: [[false, 'form']],
            target: 'new',
            view_mode: 'form',
            domain: [['res_id', '=', selectedIDs[0]], ['model', '=', this._controller.modelName]],
            context: {
                default_res_model: this._controller.modelName,
                default_res_id: selectedIDs[0],
            },
        });
    },
});

});
