odoo.define('shoot_booking.dynamic', function (require) {
    let PublicWidget = require('web.public.widget');
    const ajax = require('web.ajax');
    const session = require('web.session');

    let is_logged = false;

    session.user_has_group('base.group_user').then(function(has_group) {
        if(has_group) {
            is_logged = true;
            }
    });

    let team = this.$('input[name="team_id"]').val();
    let select = this.$('select[name="shoot_slot_id"]');

    if (select.length === 0 || team === 'undefined') {
        return {};
    }

    let Dynamic = PublicWidget.Widget.extend({
       selector: '.s_website_form',
       start: function () {
            ajax.jsonRpc('/shoot-booking/get-slots', 'call',
            {'team': team, 'is_logged': is_logged}).then(function (result) {
                    select[0].innerHTML = '';
                    for (const [key, value] of Object.entries(result)) {
                        let opt = document.createElement('option');
                        opt.value = value.id;
                        opt.innerHTML = value.dtime;
                        select[0].appendChild(opt);
                    }
            }).catch(e => {
                console.log(e);
            });
       },
    });

    PublicWidget.registry.shoot_booking_form = Dynamic;
    return Dynamic;
});
