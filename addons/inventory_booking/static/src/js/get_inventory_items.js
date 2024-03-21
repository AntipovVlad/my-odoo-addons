odoo.define('inventory_booking.dynamic', function (require) {
    const PublicWidget = require('web.public.widget');
    const ajax = require('web.ajax');

    const Dynamic = PublicWidget.Widget.extend({
       selector: '.s_website_form',
       start: function () {
            for (let i = 0; i < $("input[name='product_type']").length; i++) {
                const inventory_type = $("input[name='product_type']")[i].value;
                ajax.jsonRpc('/inventory-booking/get-inventory', 'call',
                {'booking_type': inventory_type}, {'async': false}).then(function (result) {
                    let el_id = (inventory_type == 'single') ? 'item_id' : 'set_id';
                    let sel = $(`select[name="${el_id}"]`)[0];
                    sel.innerHTML = '';

                    if (Object.keys(result).length !== 0) {
                        for (const [key, value] of Object.entries(result)) {
                            let opt = document.createElement('option');
                            opt.value = value.id;
                            opt.innerHTML = value.name;
                            sel.appendChild(opt);
                        }
                    } else {
                        let opt = document.createElement('option');
                        opt.value = '-2';
                        opt.innerHTML = 'К сожалению, доступных для выбора элементов нет';
                        sel.appendChild(opt);
                        sel.disabled = true;
                    }
                }).catch(e => {
                    console.log(e);
                });
            }
       },
    });

    PublicWidget.registry.shoot_booking_form = Dynamic;
    return Dynamic;
});
