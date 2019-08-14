/*
Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
*/
odoo.define('openapi.dashboard.tour', function (require) {
    'use strict';

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var options = {
        test: true,
        url: '/web',
        wait_for: base.ready()
    };

    var tour_name = 'openapi_dashboard';
    tour.register(tour_name, options,
                  [
                      tour.STEPS.TOGGLE_APPSWITCHER,
                      tour.STEPS.MENU_MORE,
                      {
                          trigger: '.o_app[data-menu-xmlid="base.menu_administration"], .oe_menu_toggler[data-menu-xmlid="base.menu_administration"]',
                          content: "Open Settings",
                      },
                      {
                          trigger: '.o_openapi_create',
                          content: "Click 'Add Integration'",
                      },
                      // TODO add at least one more step to be sure and Add Integration works
                  ]);
});
